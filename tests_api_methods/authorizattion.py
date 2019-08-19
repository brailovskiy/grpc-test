import grpc
from dialog_api import registration_pb2, authentication_pb2
from google.protobuf import wrappers_pb2

from sdk_testing_framework.core import SDK


class Authorize(object):
    def __init__(self):
        self.app_id = None

    def get_session_token(self, app_id_filled=None, client_pk_filled=None, app_title_filled=None, device_title_filled=None):
        """Requests for sessions token for device.
        :param device_title_filled: string
        :param app_title_filled: string
        :param client_pk_filled: bytes
        :param app_id_filled: int32
        :return: session token
        """
        print('APP_ID', app_id_filled)
        if client_pk_filled is not None:
            client_pk = client_pk_filled
        else:
            client_pk = bytes(1)
        if app_id_filled is not None:
            app_id = app_id_filled
        else:
            app_id = 10
        if app_title_filled is not None:
            app_title = app_title_filled
        else:
            app_title = 'test'
        if device_title_filled is not None:
            device_title = device_title_filled
        else:
            device_title = 'on_test'
        registration_response = SDK(unauthorized=True).registration.RegisterDevice(
            registration_pb2.RequestRegisterDevice(
                client_pk=client_pk,
                app_id=app_id,
                app_title=app_title,
                device_title=device_title
            )
        )
        print(app_id_filled)
        return registration_response

    def username_authorize(self, login, password, api_key_filled=None, device_hash_filled=None, tz_value_filled=None, app_id_filled=None, device_title_filled=None,
                           lang_filled=None, transaction_hash_filled=None):
        """
        Login and password authorization
        :param device_title_filled: string
        :param lang_filled: string locale, repeated
        :param login: string
        :param password: string
        :param api_key_filled: string
        :param device_hash_filled: bytes
        :param tz_value_filled: proto string
        :param app_id_filled: int32
        :param transaction_hash_filled: string, returns from authenticate request
        :return: user, config, config hash
        """
        if app_id_filled is not None:
            app_id = app_id_filled
        else:
            app_id = 10
        if api_key_filled is not None:
            api_key = api_key_filled
        else:
            api_key = 'key'
        if device_hash_filled is not None:
            device_hash = device_hash_filled
        else:
            device_hash = bytes(1)
        if device_title_filled is not None:
            device_title = device_title_filled
        else:
            device_title = 'on_test'
        if tz_value_filled is not None:
            tz_value = tz_value_filled
        else:
            tz_value = 'string'
        if lang_filled is not None:
            lang = lang_filled
        else:
            lang = ['EN']
        auth_response = SDK().auth.StartUsernameAuth(
            authentication_pb2.RequestStartUsernameAuth(
                username=login,
                app_id=app_id,
                api_key=api_key,
                device_hash=device_hash,
                device_title=device_title,
                time_zone=wrappers_pb2.StringValue(value=tz_value),
                preferred_languages=lang
            )
        )
        if transaction_hash_filled is not None:
            transaction_hash = transaction_hash_filled
        else:
            transaction_hash = auth_response.transaction_hash
        validation_result = SDK().auth.ValidatePassword(
            authentication_pb2.RequestValidatePassword(
                transaction_hash=transaction_hash,
                password=password
            )
        )

        return validation_result
