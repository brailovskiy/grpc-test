import os
from queue import Queue
from threading import Thread

import grpc
from google.protobuf import empty_pb2

from dialog_api import registration_pb2_grpc, messaging_pb2_grpc, media_and_files_pb2_grpc, \
    sequence_and_updates_pb2_grpc, authentication_pb2_grpc, contacts_pb2_grpc, search_pb2_grpc, users_pb2_grpc, \
    registration_pb2, authentication_pb2, sequence_and_updates_pb2, groups_pb2_grpc, obsolete_pb2_grpc, \
    profile_pb2_grpc, config_sync_pb2_grpc
from dialog_api import stickers_pb2_grpc
from shared.data_generators import Generators


class SDK:
    def __init__(self, bot_token=None, dummy_name=None, login=None, password=None, unauthorized=None):
        self.app_id = 10
        self.app_title = "ServerTestSuite"
        self.channel = grpc.secure_channel(os.environ["endpoint"], grpc.ssl_channel_credentials())
        self.registration = self.wrap_service(registration_pb2_grpc.RegistrationStub)
        if not unauthorized:
            self.token = self.get_session_token()
        else:
            self.token = None
        self.config = self.wrap_service(config_sync_pb2_grpc.ConfigSyncStub)
        self.messaging = self.wrap_service(messaging_pb2_grpc.MessagingStub)
        self.media_and_files = self.wrap_service(media_and_files_pb2_grpc.MediaAndFilesStub)
        self.updates = self.wrap_service(sequence_and_updates_pb2_grpc.SequenceAndUpdatesStub)
        self.auth = self.wrap_service(authentication_pb2_grpc.AuthenticationStub)
        self.contacts = self.wrap_service(contacts_pb2_grpc.ContactsStub)
        self.groups = self.wrap_service(groups_pb2_grpc.GroupsStub)
        self.obsolete = self.wrap_service(obsolete_pb2_grpc.ObsoleteStub)
        self.search = self.wrap_service(search_pb2_grpc.SearchStub)
        self.users = self.wrap_service(users_pb2_grpc.UsersStub)
        self.stickers = self.wrap_service(stickers_pb2_grpc.StickersStub)
        self.profile = self.wrap_service(profile_pb2_grpc.ProfileStub)
        self.user_info = None
        self.phone = None
        self.outpeers = []
        if bot_token:
            self.user_info = self.bot_authorize(bot_token)
            self.active_user_name = self.user_info.user.data.name
        elif dummy_name:
            self.user_info = self.dummy_authorize(dummy_name)
            self.active_user_name = self.user_info.user.data.name
        elif login and password:
            self.user_info = self.login_authorize(login, password)
            self.active_user_name = self.user_info.user.data.name
        elif unauthorized:
            self.user_info = None




    def gen_message(self, message):
        yield message


    def wrap_service(self, stub_func):
        """Wrapper for authenticating of gRPC service calls.

        :param stub_func: name of gRPC service
        :return: wrapped gRPC service
        """
        return AuthenticatedService(
            lambda: self.token if hasattr(self, 'token') else None,
            lambda: self.active_user_name if hasattr(self, 'active_user_name') else None,
            stub_func(self.channel)
        )

    def get_session_token(self):
        """Requests for sessions token for device.

        :return: session token
        """
        registration_response = self.registration.RegisterDevice(
            registration_pb2.RequestRegisterDevice(
                app_id=self.app_id,
                app_title=self.app_title,
                device_title=self.app_title
            )
        )
        return registration_response.token

    def bot_authorize(self, token):
        return self.auth.StartTokenAuth(
            authentication_pb2.RequestStartTokenAuth(
                token=token,
                app_id=self.app_id
            )
        )

    def dummy_authorize(self, dummy_name):
        phone = Generators.get_random_phone()
        self.phone = str(phone)
        auth_response = self.auth.StartPhoneAuth(
            authentication_pb2.RequestStartPhoneAuth(
                phone_number=phone,
                app_id=self.app_id,
                device_title=self.app_title,
                preferred_languages=['EN']
            )
        )

        try:
            self.auth.ValidateCode(
                authentication_pb2.RequestValidateCode(
                    transaction_hash=auth_response.transaction_hash
                )
            )
        except grpc.RpcError as grpc_error:
            details = grpc_error.details()
            if details == 'Unnoccupied phone number.':
                sign_up_result = self.auth.SignUp(
                    authentication_pb2.RequestSignUp(
                        transaction_hash=auth_response.transaction_hash,
                        name=dummy_name
                    )
                )

                return sign_up_result

    def login_authorize(self, login, password):
        auth_response = self.auth.StartUsernameAuth(
            authentication_pb2.RequestStartUsernameAuth(
                username=login,
                app_id=self.app_id,
                device_title=self.app_title,
                preferred_languages=['EN']
            )
        )

        validation_result = self.auth.ValidatePassword(
            authentication_pb2.RequestValidatePassword(
                transaction_hash=auth_response.transaction_hash,
                password=password
            )
        )

        return validation_result



    # def update_handler(self):
    #     for update in self.updates.SeqUpdates(empty_pb2.Empty()):
    #         up = sequence_and_updates_pb2.UpdateSeqUpdate()
    #         up.ParseFromString(update.update.value)
    #         self.update_queue.put(update)
    #
    # def get_next_update(self):
    #     yield self.update_queue.get()
    #
    # def seq_update_handler(self):
    #     for update in self.updates.SeqUpdates(empty_pb2.Empty()):
    #         up = sequence_and_updates_pb2.UpdateSeqUpdate()
    #         up.ParseFromString(update.update.value)
    #         self.seq_update_queue.put(up)
    #
    # def weak_update_handler(self):
    #     for update in self.obsolete.WeakUpdates(self.get_next_sent_weak_update()):
    #         self.weak_update_receive_queue.put(update)
    #
    # def get_next_seq_update(self):
    #     yield self.seq_update_queue.get()
    #
    # def get_next_received_weak_update(self):
    #     yield self.weak_update_receive_queue.get()
    #
    # def get_next_sent_weak_update(self):
    #     yield self.weak_update_send_queue.get()
    #
    # def send_weak_update(self, update):
    #     self.weak_update_send_queue.put(update)
    #
    # def shutdown(self):
    #     self.seq_update_thread.join()
    #     self.weak_update_thread.join()


class AuthenticatedService(object):
    """Initialization class for gRPC services.

    """

    def __init__(self, auth_token_func, user_name, stub):
        self.stub = stub
        self.auth_token_func = auth_token_func
        self.active_user_func = user_name
        for method_name in dir(stub):
            method = getattr(stub, method_name)
            if not method_name.startswith('__') and callable(method):
                setattr(self, method_name, self.__decorated(method_name, method))

    def __decorated(self, method_name, method):
        def inner(param):
            auth_token = self.auth_token_func()
            active_user = self.active_user_func()
            print('User %s calling %s ' % (active_user, method_name))
            if auth_token is not None:
                metadata = (('x-auth-ticket', auth_token),)
            else:
                metadata = None
            return method(param, metadata=metadata, timeout=10, wait_for_ready=True)

        return inner
