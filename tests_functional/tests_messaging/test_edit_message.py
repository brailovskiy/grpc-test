import allure
from hamcrest import *
import pytest


@allure.issue("SAN-54", "Edit text message")

@pytest.mark.incremental
@pytest.mark.parametrize('d_user', ["2 users"], indirect=True)
@pytest.mark.usefixtures("d_user", "update2", "update1", "send_message")
class TestEditMessage(object):
    """ UpdateMessage, updateMessageContentChanged  """

    @allure.title("User1 edit message in chat with User2")
    def test_edit_message(self, d_user):
        with allure.step('User1 edit his message in chat with User2'):
            history = d_user.load_history(d_user.u1, d_user.outpeer1)
            edit = d_user.edit_message(d_user.u1, history)
        with allure.step('Get chat history for User1 and User2'):
            hist_u1 = d_user.load_history(d_user.u1, d_user.outpeer1)
            hist_u2 = d_user.load_history(d_user.u2, d_user.outpeer2)
        with allure.step('Both users see last message edited'):
            assert hist_u1.history[0].message.textMessage.text == hist_u2.history[0].message.textMessage.text



    @allure.title("User1 and User2 gets updateMessageContentChanged")
    def test_update_edit_message(self, d_user, update1, update2):
        u1_updates = update1
        u2_updates = update2
        with allure.step('User1 gets updateMessageContentChanged after message was edited'):
            for update in u1_updates:
                if update.unboxed_update.HasField('updateMessageContentChanged'):
                    upd = update.unboxed_update.updateMessageContentChanged
                    assert upd.message.HasField('textMessage')
                    assert upd.peer.id == d_user.outpeer1.id
                    break
        with allure.step('User2 gets updateMessageContentChanged after message was edited'):
            for update in u2_updates:
                if update.unboxed_update.HasField('updateMessageContentChanged'):
                    upd = update.unboxed_update.updateMessageContentChanged
                    assert upd.message.HasField('textMessage')
                    assert upd.peer.id == d_user.outpeer2.id
                    break
