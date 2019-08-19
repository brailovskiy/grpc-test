import allure
import pytest
from hamcrest import *

# NEEDS REWORK



@allure.issue("SAN-27", "Last message")
@pytest.mark.parametrize('d_user', ["2 users"], indirect=True)
class TestLastMessage:
    """ tests for getting last message from list DP-662
     old:
     FetchDialogIndex
     LoadDialogs

     new:
     DialogListDifference
     GetLastConversationMessage
     """

    @allure.title("Last message in peer to peer chat")
    @allure.testcase("XTE-22", "Last message in peer to peer chat")
    def test_last_message_p2p(self, d_user):
        """ Tests for getting last message from p2p chats in list """
        with allure.step('User1 gets chat list by old flow'):
            chat = d_user.load_dialogs(d_user.u1)
            assert not chat is None
            chat = [item for item in chat.dialogs]
            chat = sorted(chat, key=lambda x: x.history_message.date)
        with allure.step('User1 gets chat list by new flow'):
            last_d = d_user.last_conversation_message_p2p(d_user.u1)
            last_d = [item for item in last_d.messages]
            last_d = sorted(last_d, key=lambda x: x.message.date)
        with allure.step(
                'last messages according by sender id, message text and message id'):
            assert_that([item.peer.id for item in chat]), equal_to([item.peer.id for item in last_d])
            assert_that([item.history_message.message for item in chat]), equal_to(
                [item.message.message for item in last_d])
            assert_that([item.history_message.mid for item in chat]), equal_to([item.message.mid for item in last_d])

    @allure.title("Test for getting last message in group chats")
    @allure.testcase("XTE-36", "Test for getting last message in group chats")
    def test_last_message_group(self, d_user):
        """ Tests for getting last message from group chats in list """
        with allure.step('User1 gets sorted chat list by old flow for groups'):
            chat = d_user.load_dialogs(d_user.u1)
            chat = [item for item in chat.dialogs]
            chat = sorted(chat, key=lambda x: x.history_message.date)
        with allure.step('User1 gets sorted chat list by new flow for groups'):
            last_d = d_user.last_conversation_message_group(d_user.u1)
            last_d = [item for item in last_d.messages]
            last_d = sorted(last_d, key=lambda x: x.message.date)
            #print(last_d)
        with allure.step(' Chats of User1 according by id '):
            assert_that([item.peer.id for item in chat]), equal_to([item.peer.id for item in last_d])
        with allure.step(' Last messages of User1 according by body '):
            assert_that([item.history_message.message for item in chat]), equal_to(
                [item.message.message for item in last_d])
        with allure.step(' User1 message id of last messages in chat are equal'):
            assert_that([item.history_message.mid for item in chat]), equal_to([item.message.mid for item in last_d])
        with allure.step(' Sender data of messages is not None '):
            assert_that(([item.message.sender_uid for item in last_d]), is_not(0))
        with allure.step(' Sender data of last messages in chats are equal by old and new flow '):
            assert_that([item.history_message.sender_uid for item in chat]), equal_to(
                [item.message.sender_uid for item in last_d])
