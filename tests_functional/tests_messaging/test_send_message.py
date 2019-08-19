import allure
from hamcrest import *
import pytest


# RequestSendMessage
# +------------------+--------------------------------+----------+
# |      FIELD       |              TYPE              | REPEATED |
# +------------------+--------------------------------+----------+
# | black_list       | TYPE_INT32                     | true     |
# | deduplication_id | TYPE_INT64                     | false    |
# | forward          | TYPE_MESSAGE                   | false    |
# |                  | (ReferencedMessages)           |          |
# | is_only_for_user | TYPE_INT32                     | false    |
# | message          | TYPE_MESSAGE (MessageContent)  | false    |
# | peer             | TYPE_MESSAGE (OutPeer)         | false    |
# | predicates       | TYPE_MESSAGE (SearchPredicate) | true     |
# | reply            | TYPE_MESSAGE                   | false    |
# |                  | (ReferencedMessages)           |          |
# | white_list       | TYPE_INT32                     | true     |
# +------------------+--------------------------------+----------+

# RequestSendMessage(
#                         peer=target_outpeer,
#                         deduplication_id=random.randint(0, 100000000),
#                         message=MessageContent(textMessage=TextMessage(text=text)),
#                         reply=reply,
#                         forward=forward)



@allure.issue('SAN-9', 'Send Message')

@pytest.mark.incremental
@pytest.mark.parametrize('d_user', ["2 users"], indirect=True)
@pytest.mark.usefixtures("d_user", "update1")
class TestSendMessage(object):
    """ SendMessage, UpdateMessageSent, MessageReceived, UpdateMessageReceived, MessageRead, UpdateMessageRead  """

    @allure.title("User1 sends text message to User2")
    def test_send_text_message(self, d_user):
        with allure.step('User1 send one text message'):
            msg, sent = d_user.send(d_user.u1, d_user.outpeer1)
        with allure.step('Load history for User1 and User2'):
            hist_u2 = d_user.load_history(d_user.u2, d_user.outpeer2)
            hist_u1 = d_user.load_history(d_user.u1, d_user.outpeer1)
        with allure.step('User1 and User2 has the same last message in their history'):
            assert hist_u1.history[0].message.textMessage.text == hist_u2.history[0].message.textMessage.text

    @allure.title("User1 get UpdateMessageSent")
    def test_message_sent(self, d_user, update1):
        updates = update1
        with allure.step('User1 gets update about message was sent'):
            for update in updates:
                if update.unboxed_update.HasField('updateMessageSent'):
                    assert update.unboxed_update.updateMessageSent.peer.id == d_user.outpeer1.id, "Recieved update is valid"
                    break

    @allure.title("User1 get UpdateMessageReceived when User2 calls RequestMessageReceived")
    def test_message_received(self, d_user, update1):
        updates = update1
        with allure.step('Get message history for User2'):
            hist_u2 = d_user.load_history(d_user.u2, d_user.outpeer2)
        with allure.step('User2 send receive status and User1 gets update about it'):
            d_user.receive_message(d_user.u2, d_user.outpeer2, hist_u2.history[0].date)
            for update in updates:
                if update.unboxed_update.HasField('updateMessageReceived'):
                    assert update.unboxed_update.updateMessageReceived.peer.id == d_user.outpeer1.id
                    break

    @allure.title("User1 get UpdateMessageRead when User2 calls RequestMessageRead")
    def test_message_read(self, d_user, update1):
        updates = update1
        with allure.step('Get message history for User2'):
            hist_u2 = d_user.load_history(d_user.u2, d_user.outpeer2)
        with allure.step('User2 send read status and User1 gets update about it'):
            d_user.read_message(d_user.u2, d_user.outpeer2, hist_u2.history[0].date)
            for update in updates:
                if update.unboxed_update.HasField('updateMessageRead'):
                    assert update.unboxed_update.updateMessageRead.peer.id == d_user.outpeer1.id
                    break


