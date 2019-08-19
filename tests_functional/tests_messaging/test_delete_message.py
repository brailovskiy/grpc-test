import allure
import pytest
from hamcrest import *


@allure.issue("SAN-55", "Delete text message")

@pytest.mark.incremental
@pytest.mark.parametrize('d_user', ["2 users"], indirect=True)
@pytest.mark.usefixtures("d_user", "update2", "update1", "send_message")
class TestDeleteMessage(object):
    """ UpdateMessage, updateMessageContentChanged  """

    @allure.title("User1 deletes message in chat with User2")
    def test_delete_message(self, d_user):
        with allure.step('User1 deletes his message in chat with User2'):
            hist_u1 = d_user.load_history(d_user.u1, d_user.outpeer1)
            d_user.delete_message(d_user.u1, hist_u1, delete_flag=False)
        with allure.step('Message deleted for both users'):
            hist_u1 = d_user.load_history(d_user.u1, d_user.outpeer1)
            hist_u2 = d_user.load_history(d_user.u2, d_user.outpeer2)
            assert hist_u1.history[0].message.HasField("deletedMessage")
            assert hist_u2.history[0].message.HasField("deletedMessage")

    @allure.title("User1 and User2 gets updateMessageContentChanged")
    def test_update_delete_message(self, d_user, update1, update2):
        u1_updates = update1
        u2_updates = update2
        with allure.step('User1 gets updateMessageContentChanged after deleting message'):
            for update in u1_updates:
                if update.unboxed_update.HasField('updateMessageContentChanged'):
                    upd = update.unboxed_update.updateMessageContentChanged
                    assert upd.message.HasField('deletedMessage')
                    assert upd.peer.id == d_user.outpeer1.id
                    break
        with allure.step('User2 gets updateMessageContentChanged after deleting message'):
            for update in u2_updates:
                if update.unboxed_update.HasField('updateMessageContentChanged'):
                    upd = update.unboxed_update.updateMessageContentChanged
                    assert upd.message.HasField('deletedMessage')
                    assert upd.peer.id == d_user.outpeer2.id
                    break


