import hashlib
import random
import urllib.parse
from concurrent.futures.thread import ThreadPoolExecutor
from datetime import *
from time import *
import emoji
import requests
from google.protobuf import wrappers_pb2
from dialog_api import messaging_pb2, media_and_files_pb2
from dialog_api.config_sync_pb2 import RequestGetParameters, RequestEditParameter
from dialog_api.contacts_pb2 import *
from dialog_api.groups_pb2 import *
from dialog_api.media_and_files_pb2 import FileLocation
from dialog_api.messaging_pb2 import *
from dialog_api.miscellaneous_pb2 import UPDATEOPTIMIZATION_GROUPS_V2
from dialog_api.peers_pb2 import *
from dialog_api.search_pb2 import *
from dialog_api.sequence_and_updates_pb2 import GroupMembersSubset
from dialog_api.stickers_pb2 import *
from dialog_api.users_pb2 import *
from dialog_api.profile_pb2 import *
from shared.utils import content
from sdk_testing_framework.core import *
from shared.utils.read_file_in_chunks import read_file_in_chunks
from shared.constants import DefaultValues as DV
import wget
expiration_time = datetime.now() + timedelta(seconds=20)


class Messaging(object):
    def __init__(self, users_gen, x, real_users=None):
        """
        Setting-up Pre-conditions for Test Scenario: preparing 2 or 3 authorised users and making several search calls
        for setting 'outpeer' values ( will need this in most of actions where users should interact with each other )
        """
        self.users = []
        names = ["tester1", "tester2", "tester3"]
        for _ in range(x):
            self.u = users_gen(names[_]) if real_users is not None else users_gen()
            self.users.append(self.u)
            print("... success! user - %s is authorised" % self.u.user_info.user.data.name)
        self.u1 = self.users[0]
        self.u2 = self.users[1]
        if x == 3:
            self.u3 = self.users[2]
            self.outpeer5 = self.search_d(self.u1, self.u3)
            self.outpeer3 = self.search_d(self.u2, self.u3)
            self.outpeer4 = self.search_d(self.u3, self.u2)
            self.outpeer6 = self.search_d(self.u3, self.u1)
        """ preparing data """

        self.outpeer1 = self.search_d(self.users[0], self.users[1])
        self.outpeer2 = self.search_d(self.users[1], self.users[0])

    def search_d(self, source, target):
        """
        Seacrh function - initiated user search selected user
        :param source:
        :param target:
        :return:
        """

        if target.phone is not None:
            search_result = source.contacts.SearchContacts(
                RequestSearchContacts(request=target.phone)
            )
        else:
            search_result = source.contacts.SearchContacts(
                RequestSearchContacts(request=target.user_info.user.data.nick.value))
        """ Selecting needed user from finded """
        finded = None
        #print("\tSearch results: ")
        for user in search_result.users:
            #print("\t" + user.data.name)
            if user.data.name == target.user_info.user.data.name:
                for user_peer in search_result.user_peers:
                    if user_peer.uid == user.id:
                        finded = user_peer
        return OutPeer(id=finded.uid, access_hash=finded.access_hash, type=PEERTYPE_PRIVATE)

    def search_peers(self, user, query, search_type):
        """ Peer search function - user searching contacts by query """
        values_search_type = ['group', 'contact', 'public']

        s_query = [SearchCondition(searchPieceText=SearchPieceText(query=query))]

        s_type_matching = dict(zip(
            values_search_type, [SEARCHPEERTYPE_GROUPS, SEARCHPEERTYPE_CONTACTS, SEARCHPEERTYPE_PUBLIC]))

        for s_type in search_type:
            assert s_type in values_search_type, \
                'type = {}, search_type may be list of the following values: {}'.format(s_type, values_search_type)
            s_query.append(
                SearchCondition(searchPeerTypeCondition=SearchPeerTypeCondition(peer_type=s_type_matching[s_type])))

        return user.search.PeerSearch(RequestPeerSearch(query=s_query))

    def send(self, sender, target_outpeer, num=None, reply=None, forward=None, message=None):
        """
        Send message method. If method was called without attribute :num -
        Method send one message to the chat^ returns their text and :response
        If attribute :num is not None - method sends num messages and returns print
        """
        msg = Generators.random_text_message()
        if message is not None:
            text = message
        else:
            text = msg
        if num is not None:
            for x in range(num):
                response = sender.messaging.SendMessage(
                    RequestSendMessage(
                        peer=target_outpeer,
                        deduplication_id=random.randint(0, 100000000),
                        message=MessageContent(textMessage=TextMessage(text=text)),
                        reply=reply,
                        forward=forward))
            return print("%s messages sent" % (num))
        else:
            response = sender.messaging.SendMessage(
                RequestSendMessage(
                    peer=target_outpeer,
                    deduplication_id=random.randint(0, 100000000),
                    message=MessageContent(textMessage=TextMessage(text=text)),
                    reply=reply,
                    forward=forward))
            return msg, response

    def referenced_message(self, chat):
        """ returns message from :chat, that can be used as argument for reply or forward for send() """
        return ReferencedMessages(mids=[chat.history[0].mid])

    def load_history(self, user, outpeer):
        """ :returns message history for selected user and conversation
        """
        date = int((datetime.now()).timestamp())
        # print(date)

        response = user.messaging.LoadHistory(
            RequestLoadHistory(
                peer=outpeer,
                load_mode=LISTLOADMODE_BACKWARD,
                date=0,
                limit=10))
        return response

    def read_message(self, user, outpeer, date):
        """ read message request """
        response = user.messaging.MessageRead(
            RequestMessageRead(
                peer=outpeer,
                date=date
            )
        )
        return response

    def receive_message(self, user, outpeer, date):
        """ receive message request """
        response = user.messaging.MessageReceived(
            RequestMessageReceived(
                peer=outpeer,
                date=date
            )
        )
        return response

    def edit_message(self, user, chat):
        """ Edit message request """
        txt = Generators.random_text_message()
        edit = user.messaging.UpdateMessage(
            RequestUpdateMessage(
                mid=chat.history[0].mid,
                updated_message=MessageContent
                (textMessage=TextMessage
                (text=txt)),
                last_edited_at=chat.history[0].date))
        return txt, edit

    def delete_message(self, user, chat, delete_flag=None):
        """ Delete message request """
        response = user.messaging.UpdateMessage(
            RequestUpdateMessage(
                mid=chat.history[0].mid,
                updated_message=MessageContent
                (deletedMessage=DeletedMessage
                (is_local=wrappers_pb2.BoolValue(value=delete_flag))),
                last_edited_at=chat.history[0].date))
        return response

    def dialog_index(self, user):
        """ loads indices of dialogs for selected user """
        while True:
            response = user.messaging.FetchDialogIndex(RequestFetchDialogIndex())
            if len(response.dialog_indices) is not 0:
                return response
            now = datetime.now()
            if now > expiration_time:
                return None

    def load_dialogs(self, user):
        """ Loads dialog list"""
        sleep(0.5)
        indices = self.dialog_index(user).dialog_indices
        response = user.messaging.LoadDialogs(
            RequestLoadDialogs(
                peers_to_load=[item.peer for item in indices]
            ))
        return response



    def load_dialogs_with_wait(self, user, channel_id):
        """ Load dialogs with handling by time
        """
        i = 0
        chats = chats_id = None
        while i < 9:
            chats = self.load_dialogs(user)
            chats_id = [dialog.id for dialog in chats.groups]
            if channel_id in chats_id:
                return chats, chats_id
            sleep(1.5)
            i = i + 1
        return chats, chats_id

    def list_difference(self, user):
        """ Loading missing dialogs """
        response = user.messaging.DialogListDifference(messaging_pb2.RequestDialogListDifference(
            from_clock=int((datetime.today() - timedelta(1)).timestamp()
                           )))
        return response


    def dialog_difference(self, user):
        """ Loading missing messages"""
        response = user.updates.GetDialogsDifference(sequence_and_updates_pb2.RequestGetDialogsDifference(
            clock=int((datetime.today() - timedelta(1)).timestamp()
                      )))
        return response


    def last_conversation_message_p2p(self, user):
        """ Loading last message in peer to peer conversation
        :param UserOutPeer"""
        user_peers = [entry.peer for entry in self.list_difference(user).entries if
                      entry.peer.type == PEERTYPE_PRIVATE]
        response = user.messaging.GetLastConversationMessages(messaging_pb2.RequestGetLastConversationMessages(
            peers=user_peers
        ))
        return response

    def last_conversation_message_group(self, user):
        """ Loading last message in group conversation
        :param GroupOutPeer"""
        group_peers = [entry.peer for entry in self.list_difference(user).entries if
                       entry.peer.type == PEERTYPE_GROUP]

        response = user.messaging.GetLastConversationMessages(messaging_pb2.RequestGetLastConversationMessages(
            peers=group_peers
        ))
        return response


    def edit_profile_about(self, user, about=None):
        """
        Request for edit about field in private profile
        :param user: user who edit profile
        :param about: new value about field
        :return:
        """
        if about is None:
            about = Generators.get_random_about()
        user.profile.EditAbout(RequestEditAbout(
            about=wrappers_pb2.StringValue(value=about)))
        return about

    def edit_avatar_profile(self, user, avatar):
        """
        Request for edit avatar in private profile
        :param user: user who edit profile
        :param avatar: new avatar
        :return:
        """
        file_location = self.upload_file(user, avatar)
        res = user.profile.EditAvatar(RequestEditAvatar(
            file_location=file_location
        ))
        return res

    def remove_avatar_profile(self, user):
        """
        Request for remove avatar in private profile
        :param user: user who edit profile
        :return:
        """
        res = user.profile.RemoveAvatar(RequestRemoveAvatar())
        return res

    def load_user_data(self, user):
        """ Loading user's data for peer to peer dialogs list"""
        entries = self.list_difference(user).entries
        users = [entry.peer for entry in entries if entry.peer.type == PEERTYPE_PRIVATE]
        response = user.users.LoadUserData(RequestLoadUserData(claims=[RequestLoadUserData.Claim(
            user_peer=peer,
            p2p=True
        ) for peer in users]))
        return response


    def load_user_data_groups(self, user):
        """ Loading user's data for group dialogs list"""
        pairs = self.last_conversation_message_group(user).messages
        response = user.users.LoadUserData(RequestLoadUserData(claims=[RequestLoadUserData.Claim(
            user_peer=Peer(id=pair.message.sender_uid, type=PEERTYPE_GROUP),
            group_member=pair.peer
        ) for pair in pairs]))
        return response


    def referenced_entites_groups_new(self, user):
        """ Referenced entities for groups"""
        group_id = self.list_difference(user).entries[1].peer.id
        response = user.updates.GetReferencedEntitites(sequence_and_updates_pb2.RequestGetReferencedEntitites(
            group_members=[GroupMembersSubset
                (group_peer=GroupOutPeer(
                group_id=group_id))],
            groups=[GroupOutPeer(
                group_id=group_id,
                access_hash=0)])
        )
        return response


    def create_group(self, user, user_outpeers=None, group_type=None, with_shortname=None):
        """ Request for creating group """
        title = Generators.random_group_name()
        shortname = None
        if with_shortname is True:
            shortname = wrappers_pb2.StringValue(value=title)
        if user_outpeers is not None:
            user_outpeers = [UserOutPeer(uid=u.id, access_hash=u.access_hash) for u in user_outpeers]
        response = user.groups.CreateGroup(RequestCreateGroup(
            rid=random.randint(0, 100000000),
            space_id=None,
            title=title,
            users=user_outpeers,
            group_type=group_type,
            username=shortname,
            optimizations=[UPDATEOPTIMIZATION_GROUPS_V2]
        ))
        return response

    def add_group_members(self, user, users, group):
        """ Request add group member"""
        response = user.groups.InviteUser(RequestInviteUser(
            rid=random.randint(0, 100000000),
            group_peer=GroupOutPeer(
                group_id=group.id,
                access_hash=group.access_hash),
            user=UserOutPeer(
                uid=users.id,
                access_hash=users.access_hash)
        ))
        return response

    def remove_group_member(self, user, deleted_user, group):
        """ Request kick user from group"""
        response = user.groups.KickUser(RequestKickUser(
            rid=random.randint(0, 100000000),
            group_peer=GroupOutPeer(
                group_id=group.id,
                access_hash=group.access_hash),
            user=UserOutPeer(
                uid=deleted_user.id,
                access_hash=deleted_user.access_hash)
        ))
        return response

    def leave_group(self, user, group):
        """ Request user for leaving group"""
        user.groups.LeaveGroup(RequestLeaveGroup(
            group_peer=GroupOutPeer(
                group_id=group.id,
                access_hash=group.access_hash
            )))

    def join_group_by_peer(self, user, group_id, group_access):
        """ User joins group by finding groups' peer """
        response = user.groups.JoinGroup(RequestJoinGroupByPeer(
            peer=GroupOutPeer(
                group_id=group_id,
                access_hash=group_access
            )
        ))
        return response

    def load_group_members(self, user, group, limit=10):
        """ Request for group members with custom limit
        """
        response = user.groups.LoadMembers(RequestLoadMembers(
            group=GroupOutPeer(
                group_id=group.id,
                access_hash=group.access_hash),
            limit=limit
        ))
        return response

    def load_group_members_with_wait(self, user, group, expected_count, limit=10):
        """ Loading group members with handling by time
        """
        i = 0
        while i < 10:
            result = self.load_group_members(user, group, limit)
            members = [x.uid for x in result.members]
            count = len(members)
            if count == expected_count:
                return members
            sleep(1)
            i = i + 1
        return members

    def load_stickers(self, user, clock=None):
        """
        Request load available stickers
        :param user:
        :param clock:
        :return:
        """
        response = user.stickers.LoadAcesssibleStickers(RequestLoadAcesssibleStickers(
            from_clock=clock
        ))
        return response

    def new_sticker_pack(self, user, title):
        """
        Request for adding new stickerpack
        :param user:
        :param title:
        :return:
        """
        response = user.stickers.AddStickerCollection(RequestAddStickerCollection(
            title=title
        ))
        return response

    def upload_file_chunk(self, user, part_number, chunk, upload_key):
        """Upload file chunk.
        :param user: uploader
        :param part_number: number of chunk (>=0)
        :param chunk: chunk content
        :param upload_key: upload key (need to be received from RequestGetFileUploadUrl request before uploading)
        :return: Response of HTTP PUT request if success or None otherwise
        """

        url = user.media_and_files.GetFileUploadPartUrl(
            media_and_files_pb2.RequestGetFileUploadPartUrl(
                part_number=part_number,
                part_size=len(chunk),
                upload_key=upload_key
            )
        ).url
        put_response = requests.put(
            url,
            data=chunk,
            headers={'Content-Type': 'application/octet-stream'},
        )

        if put_response.status_code != 200:
            print('Can\'t upload file chunk #{}'.format(part_number))
            return None

        return put_response

    def upload_file(self, user, file, max_chunk_size=1024 * 1024, parallelism=10):
        """Upload file for sending.
        :param user: uploader
        :param file: path to file
        :param max_chunk_size: maximum size of one chunk (default 1024 * 1024)
        :param parallelism: number of uploading threads (default: 10)
        :return: FileLocation object if success or None otherwise
        """

        upload_key = user.media_and_files.GetFileUploadUrl(
            media_and_files_pb2.RequestGetFileUploadUrl(
                expected_size=os.path.getsize(file)
            )
        ).upload_key

        with ThreadPoolExecutor(max_workers=parallelism) as executor:
            result = list(
                executor.map(
                    lambda x: self.upload_file_chunk(user, *x),
                    (
                        (part_number, chunk, upload_key) for part_number, chunk in enumerate(
                        read_file_in_chunks(file, max_chunk_size)
                    )
                    )
                )
            )

            if not all(result):
                return None

        asd = user.media_and_files.CommitFileUpload(
            media_and_files_pb2.RequestCommitFileUpload(
                upload_key=upload_key,
                file_name=os.path.basename(file)
            )
        ).uploaded_file_location
        print(asd)
        return asd

    def share_file(self, user, target_outpeer, file):

        data = {
            'peer': 'private_' + str(target_outpeer.id) + ':' + str(target_outpeer.access_hash),
        }

        files = {
            'file': open(file, 'rb')
        }

        return requests.post(
            os.environ['SHARING_URL'] + '/v1/messaging?token=' + urllib.parse.quote(user.token),
            # если в SHARING_URL нет приставки '/v1/messaging', ее нужно добавить в конец URL'а
            data=data,
            files=files
        )

    def send_file(self, user, target_outpeer, file):
        """Send file to current peer.

        :param peer: receiver's peer
        :param file: path to file
        :return: value of SendMessage response object
        """
        location = self.upload_file(user, file)
        msg = messaging_pb2.MessageContent()

        msg.documentMessage.CopyFrom(
            content.get_document_content(file, location)
        )

        return user.messaging.SendMessage(messaging_pb2.RequestSendMessage(
            peer=target_outpeer,
            deduplication_id=random.randint(0, 100000000),
            message=msg
        ))

    def send_image(self, user, target_outpeer, file):
        """Send image as image (not as file) to current peer.

        :param peer: receiver's peer
        :param file: path to image file
        :return: value of SendMessage response object
        """

        location = self.upload_file(user, file)
        msg = messaging_pb2.MessageContent()

        msg.documentMessage.CopyFrom(
            content.get_image_content(str(file), location)
        )

        return user.messaging.SendMessage(messaging_pb2.RequestSendMessage(
            peer=target_outpeer,
            deduplication_id=random.randint(0, 100000000),
            message=msg
        ))

    def send_video(self, user, target_outpeer, file):
        """Send image as image (not as file) to current peer.

        :param peer: receiver's peer
        :param file: path to image file
        :return: value of SendMessage response object
        """

        location = self.upload_file(user, file)
        msg = messaging_pb2.MessageContent()

        msg.documentMessage.CopyFrom(
            content.get_video_content(str(file), location)
        )

        return user.messaging.SendMessage(messaging_pb2.RequestSendMessage(
            peer=target_outpeer,
            deduplication_id=random.randint(0, 100000000),
            message=msg
        ))

    def hasher(self, file):
        """Get md5 sum.

        """
        with open(file, 'rb') as fh:
            m = hashlib.md5(fh.read())
            print(os.path.getsize(file))
            print(m.hexdigest())
        return m.hexdigest()

    def download_link(self, user, outpeer):
        """ Download file by reciever
        """
        while True:
            hist = self.load_history(user, outpeer)
            history =[item.message for item in hist.history]
            if len(history) > 0:
                location = hist.history[0].message.documentMessage
                url =  user.media_and_files.GetFileUrl(media_and_files_pb2.RequestGetFileUrl(
                    file=FileLocation(
                        file_id=location.file_id,
                        access_hash=location.access_hash
                    )))
                if url is not None:
                    return url
            now = datetime.now()
            if now > expiration_time:
                return None
            sleep(0.5)

    def download(self, user, outpeer):
        """ Download from CDN"""
        url = self.download_link(user, outpeer).url
        load = wget.download(url, out=DV.downloads)
        print(load)
        return load

    def download_file_by_file_location(self, user, file_location):
        url = user.media_and_files.GetFileUrl(media_and_files_pb2.RequestGetFileUrl(
            file=file_location)).url
        load = wget.download(url, out=DV.downloads)
        return load

    def get_parameters(self, user):
        """ Request for getting all parameters of user
        :param user: user who requests their config
        :return config set in seq update"""
        params = user.config.GetParameters(RequestGetParameters(

        ))
        return params

    def send_draft(self, user, outpeer, draft_type, msg):
        """
        Request for send draft
        :param user: user that tyoed draft
        :param outpeer: user from conversation
        :param draft_type: group or private
        :param msg: draft body in string
        :return:
        """
        msg = msg
        draft = user.config.EditParameter(RequestEditParameter(
            key=draft_type + str(outpeer),
            value=wrappers_pb2.StringValue(value=msg)
        ))
        return draft, msg

    def set_reaction(self, user, outpeer, mid, code):
        """
        Request for set reaction to message
        :param user: user who sets reaction
        :param outpeer: outpeer of message author
        :param mid: message id of reaction target
        :param code: EMOJI in string or random emoji if None
        :return: ReactionResponse
        """
        if code is not None:
            e = emoji.emojize(code)
        else:
            e = Generators.random_emoji()
        return user.messaging.MessageSetReaction(RequestMessageSetReaction(
            peer=outpeer,
            mid=mid,
            code=e
        ))

    def remove_reaction(self, user, outpeer, mid, code):
        """
        Request for set reaction to message
        :param user: user who sets reaction
        :param outpeer: outpeer of message author
        :param mid: message id of reaction target
        :return: ReactionResponse
        """
        return user.messaging.MessageRemoveReaction(RequestMessageRemoveReaction(
            peer=outpeer,
            mid=mid,
            code=emoji.emojize(code)
        ))
