import allure
import pytest
from hamcrest import *


@allure.issue("SAN-44", "Remove user from group")
@pytest.mark.parametrize('d_user', ["2 users"], indirect=True)
class TestRemoveUserFromGroup(object):
    """ Removing users from group by owner """

    @allure.title("Test kick user from group")
    @allure.testcase("XTE-21", "Test kick user from group")
    def test_remove_user_from_public_group(self, d_user, _group):
        """  Remove user from public group by owner"""
        with allure.step('User1 creates public group with User2'):
            new_group = _group
        with allure.step('User1 remove User2'):
            d_user.remove_group_member(d_user.u1, d_user.outpeer1, new_group.group)
        with allure.step('Amount of members equal to 1'):
            members = d_user.load_group_members_with_wait(d_user.u1, new_group.group, expected_count=1)
            assert_that(members, has_length(1))
        with allure.step('User2 not listed on group'):
            assert_that(members, not_(has_item(d_user.u2.user_info.user.id)))

    @allure.title("Test kick user from group update")
    def test_update_for_removing_user(self, d_user, _group, update2):
        updates = update2
        new_group = _group
        with allure.step('User2 gets update about exclusion from the group'):
            for update in updates:
                if update.unboxed_update.HasField('updateGroupUserKickObsolete'):
                    kick_update = update.unboxed_update.updateGroupUserKickObsolete
                    assert_that(kick_update.group_id, equal_to(new_group.group.id))
                    assert_that(kick_update.kicker_uid, equal_to(d_user.u1.user_info.user.id))
                    break
