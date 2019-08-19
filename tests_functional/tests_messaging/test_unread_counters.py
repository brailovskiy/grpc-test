import allure
from hamcrest import *
import pytest


@allure.issue("SAN-38", "Counters")

@pytest.mark.incremental
@pytest.mark.parametrize('d_user', ["2 users"], indirect=True)
@pytest.mark.usefixtures("d_user", "update2", "update1")
class TestUnreadCounters:
    """ Tests for unread counters """

    @allure.title("increase unread counter when user gets new messages")
    def test_counter_on_message(self, d_user, update1):
        updates = update1
        with allure.step('User1 gets current unread counter for chat with User2'):
            chat_list = d_user.list_difference(d_user.u1)
            chat_with_u2 = [entry for entry in chat_list.entries if entry.peer.id == d_user.u2.user_info.user.id]
            counter = chat_with_u2[0].unread_count
            print(chat_with_u2[0].unread_count)
        with allure.step('User2 send 5 messages to User1'):
            d_user.send(d_user.u2, d_user.outpeer2, 5)
        with allure.step('User1 gets updates for new messages, counter increased to 5'):

            for update in updates:

                if update.unboxed_update.updateMessage.peer.id == d_user.u2.user_info.user.id:
                    print(update.unboxed_update.updateMessage.counter.value)
                if update.unboxed_update.updateMessage.counter.value == counter + 5:
                    print("ALL MESSAGES FOUND")
                    break
        with allure.step('User1 check unread counter for chat with user2, conter increasee to 5'):
            chat_list = d_user.list_difference(d_user.u1)
            chat_with_u2 = [entry for entry in chat_list.entries if entry.peer.id == d_user.u2.user_info.user.id]
            counter_new = chat_with_u2[0].unread_count
            print("counter before: %s \ncounter now: %s" % (counter, counter_new))
            assert_that(counter_new == counter + 5)

    @allure.title("Test partial read of conversation")
    def test_partial_read(self, d_user, update1):
        updates = update1
        with allure.step('User2 send 5 messages to User1'):
            d_user.send(d_user.u2, d_user.outpeer2, 5)
        with allure.step('User1 get updates about new messages from User2'):
            count = 0
            for update in updates:
                if update.unboxed_update.updateMessage.peer.id == d_user.u2.user_info.user.id:
                    print(update.unboxed_update.updateMessage.counter.value)
                    count += 1
                if count >= 5:
                    print("ALL MESSAGES FOUND")
                    break
        with allure.step('User1 check unread counter'):
            chat_list = d_user.list_difference(d_user.u1)
            chat_with_u2 = [entry for entry in chat_list.entries if entry.peer.id == d_user.u2.user_info.user.id]
            print(chat_with_u2[0])
        with allure.step('User1 read 3 messages from chat with User2'):
            history = d_user.load_history(d_user.u1, d_user.outpeer1)
            d_user.read_message(d_user.u1, d_user.outpeer1, history.history[2].date)
        with allure.step('User1 check unread counter'):
            chat_list_new = d_user.list_difference(d_user.u1)
            chat_with_u2_new = [entry for entry in chat_list_new.entries if
                                entry.peer.id == d_user.u2.user_info.user.id]
            print(chat_with_u2_new[0])
        with allure.step('New unread counter value equals to 2 '):
            assert_that(chat_with_u2_new[0].unread_count == 2)
