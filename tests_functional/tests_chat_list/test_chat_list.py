import pytest
import allure
from hamcrest import *


# NEEDS REWORK


@allure.issue("SAN-5", "Chat list tests")
@pytest.mark.parametrize('d_user', ["2 users"], indirect=True)
class TestChatList:
    """ Tests for getting chat list DP-660
          old:
     FetchDialogIndex
     LoadDialogs
          new:
     DialogListDifference
     """

    @allure.title("Test for user chat list")
    @allure.testcase("XTE-15", "Test for user chat list")
    def test_chat_list(self, d_user):
        """ Tests for group and p2p chats in chat list and comparing LoadDialogs and ListDifference methods """
        with allure.step('Get chat list with old flow - RequestLoadDialogs'):
            chats_old = d_user.load_dialogs(d_user.u1)
            chats_old = sorted([items.peer.id for items in chats_old.dialogs])
            #print(chats_old)
        with allure.step('Get chat list with new flow - RequestListDifference'):
            chats_new = d_user.list_difference(d_user.u1)
            chats_new = sorted([items.peer.id for items in chats_new.entries])
            #print(chats_new)
        with allure.step('User 1 have chat list with one p2p & one group chat'):
            assert_that(chats_new, is_not(None))
            assert_that(chats_new[-2:], equal_to(chats_old[-2:]))
