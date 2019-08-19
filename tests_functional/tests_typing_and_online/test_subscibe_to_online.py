import allure
from hamcrest import assert_that, equal_to
import pytest
from shared import update_helpers


@allure.issue("SAN-37", "Online")
@pytest.mark.parametrize('d_user', ["2 users"], indirect=True)
class TestSubscribeToOnline:
    """Tests for subscribing on weak updates for 'online' user status"""

    @allure.title("Test for online status")
    @allure.testcase("XTE-30", "Test for online status")
    def test_subscribe_online(self, d_user):
        """ Test for online status"""

        with allure.step('User1 subscribing to online statuses from User2'):
            message = update_helpers.make_subscribe_to_onlines(d_user.outpeer1.id, d_user.outpeer1.access_hash)
            updates = update_helpers.UpdateHelpers.weak_updates_helper(d_user.u1.obsolete, message)

        with allure.step('User2 send onlines'):
            message_u2 = update_helpers.send_my_online()
            updates2 = update_helpers.UpdateHelpers.weak_updates_helper(d_user.u2.obsolete, message_u2)

        with allure.step('User1 receive online statuses from User2'):
            for update in updates:
                print(update)
                status = update.userLastSeen
                if status.isOnline:
                    assert_that(status.userId, equal_to(d_user.outpeer1.id))
                    break
