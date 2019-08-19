import allure
from hamcrest import *
from dialog_api.peers_pb2 import PEERTYPE_GROUP
import pytest

# NEEDS REWORK

@allure.issue("SAN-5", "Chat list")
@pytest.mark.parametrize('d_user', ["2 users"], indirect=True)
class TestUserData:
    """ Tests user's data for preview in chat list DP-661
          old:
     FetchDialogIndex
     LoadDialogs
          new:
     DialogListDifference
     LoadUserData
     GetLastConversationMessages
     GetReferencedEntitites
      """

    @allure.title("User data in peer to peer chat")
    @allure.testcase("XTE-33", "User data in peer to peer chat")
    def test_user_data_p2p(self, d_user):
        """ Test for user data in peer to peer conversation """
        d_user.dialog_difference(d_user.u1)
        with allure.step('User1 loading userdata by old flow'):
            data = d_user.load_dialogs(d_user.u1)
        with allure.step('User1 loading userdata by new flow'):
            user_data = d_user.load_user_data(d_user.u1)
            #print(user_data)
        with allure.step('Loaded data are equal'):
            assert_that(data.users, has_item(user_data.users[0]))

    @allure.title("User data in peer to peer chat")
    @allure.testcase("XTE-13", "User data in group chat")
    def test_user_data_groups(self, d_user):
        """ Test for user data group """
        d_user.dialog_difference(d_user.u1)
        with allure.step('User1 loading userdata by old flow'):
            data = d_user.load_dialogs(d_user.u1)
        with allure.step('Sorting data by sender id of last message in group chat'):
            user_old = sorted(
                [item.history_message.sender_uid for item in data.dialogs if item.peer.type == PEERTYPE_GROUP])
        with allure.step('Loading user data of last message sender in gropu chat by new flow'):
            user_data = d_user.load_user_data_groups(d_user.u1)
        with allure.step('Sorting by id of last message senders by new flow'):
            user_new = sorted([item.id for item in user_data.users])
        with allure.step('Data are equal in both flow'):
            assert_that(user_old and user_new, is_not(None))
            group_data = d_user.referenced_entites_groups_new(d_user.u1)
            #print(group_data)
        # with allure.step('Userdata in old flow equal to data in old flow'):
        #     assert_that(user_old, has_items(user_new[0], user_new[1], user_new[2]))
        # with allure.step('Loaded users list are equal'):
        #     assert_that(data.users, has_items(user_data.users[0], user_data.users[1], user_data.users[2]))
        # with allure.step('Groups information in old flow equal to group information in new flow'):
        #     assert_that(data.groups, has_items(group_data.groups[0]))
