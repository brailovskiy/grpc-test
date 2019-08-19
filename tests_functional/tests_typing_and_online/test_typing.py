import allure
from hamcrest import assert_that, equal_to
import pytest
from shared import update_helpers


@allure.issue("SAN-37", "Typing")
@pytest.mark.parametrize('d_user', ["2 users"], indirect=True)
class TestTypingStatus:
    """Tests for subscribing on weak updates for 'typing' user status"""

    @allure.title("Test for typing status")
    @allure.testcase("XTE-26", "Test for typing status")
    def test_typing(self, d_user):
        """ Test for typing status"""
        with allure.step('User1 subscribe for typing statuses from User2'):
            message = update_helpers.make_subscribe_to_typing(d_user.outpeer1.id, d_user.outpeer1.access_hash)
            updates = update_helpers.UpdateHelpers.weak_updates_helper(d_user.u1.obsolete, message)

        with allure.step('User2 sending typing statuses'):
            message_u2 = update_helpers.send_my_typing(d_user.outpeer2.id, d_user.outpeer2.access_hash)
            updates2 = update_helpers.UpdateHelpers.weak_updates_helper(d_user.u2.obsolete, message_u2)

        with allure.step('User1 receive typing statuses from User2 that types a text'):
            for update in updates:
                print(update)
                typing = update.typing
                if typing.isTyping:
                    assert_that(typing.userId, equal_to(d_user.outpeer1.id))
                    assert_that(typing.peer.id, equal_to(d_user.outpeer2.id))
                    break
