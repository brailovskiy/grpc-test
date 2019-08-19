import allure
from dialog_api.peers_pb2 import OutPeer, PEERTYPE_GROUP
from hamcrest import *
import pytest


@allure.issue("SAN-29", "Forward message")
@pytest.mark.parametrize('d_user', ["2 users"], indirect=True)
class TestForwardMessage:
    """ Tests for forwarding messages """

    @allure.title("Test forward message to current chat")
    @allure.testcase("XTE-28", "Test forward message to current chat")
    def test_forward_message_here(self, d_user, update1):
        """ Forward message to current chat """
        updates = update1
        with allure.step('User1 send message to User2'):
            message = d_user.send(d_user.u1, d_user.outpeer1)
        with allure.step('User1 forward message to current char'):
            history = d_user.load_history(d_user.u1, d_user.outpeer1)
            message1 = d_user.referenced_message(history)
            msg = d_user.send(d_user.u1, d_user.outpeer1, forward=message1)
        with allure.step('User1 gets update: user id equal to user that forwarded message'):
            for update in updates:
                sent = update.unboxed_update.updateMessageSent
                if sent.HasField('prev_mid'):
                    assert sent.peer.id == d_user.outpeer1.id
                    break
        with allure.step('Loading forwarded message history'):
            send_fwd = d_user.load_history(d_user.u1, d_user.outpeer1)
            rec_fwd = d_user.load_history(d_user.u2, d_user.outpeer2)
        with allure.step('Message id of forwarded equal to message id of original'):
            assert_that(send_fwd.history[0].forward.mids[0],
                        equal_to(message[1].message_id))
            assert_that(rec_fwd.history[0].forward.mids[0],
                        equal_to(message[1].message_id))
        with allure.step('Text of original message equal to tex of forwarded'):
            assert_that(send_fwd.history[0].message.textMessage.text,
                        equal_to(msg[0]))
            assert_that(rec_fwd.history[0].message.textMessage.text,
                        equal_to(msg[0]))

    @allure.title("Test forward message to group")
    def test_forward_message_to_group(self, d_user, _group, update1, update2):
        """ Forward message from private chat to group """
        updates = update1
        updates2 = update2
        group_info = _group
        outpeer = OutPeer(id=group_info.group.id, access_hash=group_info.group.access_hash, type=2)
        with allure.step('User1 send message to User2'):
            message = d_user.send(d_user.u1, d_user.outpeer1)[1]
        with allure.step('User2 load history'):
            history = d_user.load_history(d_user.u1, d_user.outpeer1)
            message1 = d_user.referenced_message(history)
        with allure.step('User2 forward message to created group'):
            d_user.send(d_user.u1,
                        target_outpeer=outpeer,
                        forward=message1)
        with allure.step('User1 load group history'):
            group_history = d_user.load_history(d_user.u1, outpeer=outpeer).history[0]
        with allure.step('User1 get update about forward'):
            for update in updates:
                peer = update.unboxed_update.updateMessageSent.peer
                if peer.type == 2:
                    assert_that(peer.id, equal_to(group_info.group.id))
                    break
        with allure.step('Forwarded message listed in history'):
            assert_that(message.message_id, equal_to(group_history.forward.mids[0]))
        with allure.step('User2 get update about forward'):
            for update in updates2:
                msg = update.unboxed_update.updateMessage
                if msg.HasField('forward'):
                    assert_that(msg.forward.mids[-1], equal_to(message.message_id))
                    break

    @allure.title("Test forward message from channel to p2p conversation")
    def test_forward_message_from_channel(self, d_user, _channel, update1):
        """ Forward message from private chat to group """
        updates = update1
        chan_info = _channel
        outpeer = OutPeer(id=chan_info.group.id, access_hash=chan_info.group.access_hash, type=2)
        with allure.step('User1 send message to his channel'):
            message = d_user.send(d_user.u1, target_outpeer=outpeer)[1]
        with allure.step('User2 load history in channel'):
            history = d_user.load_history(d_user.u1, outpeer=outpeer)
            message1 = d_user.referenced_message(history)
        with allure.step('User2 forward message to User1'):
            d_user.send(d_user.u2, d_user.outpeer2, forward=message1)
        with allure.step('User1 load conversation history with User2'):
            conv_history = d_user.load_history(d_user.u1, d_user.outpeer1).history[0]
        with allure.step('Forwarded message listed in history'):
            assert_that(message.message_id, equal_to(conv_history.forward.mids[0]))
        with allure.step('User1 get update about forward'):
            for update in updates:
                msg = update.unboxed_update.updateMessage
                if msg.HasField('forward'):
                    assert_that(msg.forward.mids[-1], equal_to(message.message_id))
                    break
