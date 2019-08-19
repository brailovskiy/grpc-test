import allure
from hamcrest import *
import pytest


@allure.issue("SAN-24", "Reply")
@pytest.mark.parametrize('d_user', ["2 users"], indirect=True)
class TestReplyToMessage:
    """ Tests for reply to message"""

    @allure.title("Test reply to message")
    @allure.testcase("XTE-38", "Test reply to message")
    def test_reply_to_message_privatechat(self, d_user, update1):
        """ Test for reply to one message"""
        updates = update1
        with allure.step('User1 send message to user2'):
            message = d_user.send(d_user.u1, d_user.outpeer1)
        with allure.step('User1 reply to his message'):
            history = d_user.load_history(d_user.u1, d_user.outpeer1)
            message1 = d_user.referenced_message(history)
            msg = d_user.send(d_user.u1, d_user.outpeer1, reply=message1)
        with allure.step('Both users loading history'):
            send_fwd = d_user.load_history(d_user.u1, d_user.outpeer1)
            rec_fwd = d_user.load_history(d_user.u2, d_user.outpeer2)
        with allure.step(
                'User1 gets update: id equal to replied user'):
            for update in updates:
                sent = update.unboxed_update.updateMessageSent
                if sent.HasField('prev_mid'):
                    assert sent.peer.id == d_user.outpeer1.id
                    break
        with allure.step(
                'Message id of replied and original message are equal'):
            assert_that(send_fwd.history[0].reply.mids[0],
                        equal_to(message[1].message_id))
            assert_that(rec_fwd.history[0].reply.mids[0],
                        equal_to(message[1].message_id))
        with allure.step('Text of replied message are equal'):
            assert_that(send_fwd.history[0].message.textMessage.text,
                        equal_to(msg[0]))
            assert_that(rec_fwd.history[0].message.textMessage.text,
                        equal_to(msg[0]))
