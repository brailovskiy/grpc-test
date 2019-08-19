from time import sleep
import allure
import pytest
from hamcrest import *


@allure.issue("SAN-44", "Leave Group")
@pytest.mark.xfail(reason='Broken logic of leaving groups')
@pytest.mark.incremental
@pytest.mark.usefixtures("d_user", "_group", "leave_group", "update1", "update2")
@pytest.mark.parametrize('d_user', ["2 users"], indirect=True)
class TestLeaveGroup(object):
    """ Leaving users from group """

    @allure.title("Test Leave users from group chat")
    @allure.testcase("XTE-19", "Test Leave users from group chat")
    def test_leave_public_group(self, d_user, _group, leave_group, update1, update2):
        """  Leave users from group chat"""
        new_group = _group
        leave = leave_group
        with allure.step('Amount of members equal to 1'):
            d_user.load_group_members_with_wait(d_user.u1, new_group.group, expected_count=1)
            members = d_user.load_group_members(d_user.u1, new_group.group)
            assert_that(members, has_length(1))
        with allure.step('User2 not listed in group members list'):
            assert_that(members, not_(has_item(d_user.u2.user_info.user.id)))

    @allure.title("Test User1 obsolete update")
    def test_leave_user1_update_obsolete(self, d_user, _group, update1):
        updates1 = update1
        new_group = _group
        with allure.step('User1 obsolete update for leaving'):
            for update in updates1:
                print(update)
                if update.unboxed_update.HasField('updateGroupUserLeaveObsolete'):
                    update_members = update.unboxed_update.updateGroupMembersCountChanged
                    assert_that(update_members.group_id, equal_to(new_group.group.id))
                    assert_that(update_members.members_count, equal_to(1))
                    break

    @allure.title("Test User2 obsolete update")
    def test_leave_user2_update_obsolete(self, d_user, _group, update2):
        updates2 = update2
        new_group = _group
        with allure.step('User2 obsolete update for leaving'):
            for update in updates2:
                if update.unboxed_update.HasField('updateGroupUserLeaveObsolete'):
                    update_members = update.unboxed_update.updateGroupMembersCountChanged
                    assert_that(update_members.group_id, equal_to(new_group.group.id))
                    assert_that(update_members.members_count, equal_to(1))
                    break

    @allure.title("Test User1 service update")
    def test_leave_user1_service_update(self, d_user, _group, update1):
        updates1 = update1
        new_group = _group
        with allure.step('User1 obsolete update for leaving'):
            for update in updates1:
                if update.unboxed_update.message.serviceMessage.text == "User left the group":
                    update_members = update.unboxed_update.updateMessage
                    assert_that(update_members.group_id, equal_to(new_group.group.id))
                    assert_that(update_members.members_count, equal_to(1))
                    break

    @allure.title("Test User2 service update")
    def test_leave_user2_service_update(self, d_user, _group, update2):
        updates2 = update2
        new_group = _group
        with allure.step('User1 obsolete update for leaving'):
            for update in updates2:
                if update.unboxed_update.message.serviceMessage.text == "User left the group":
                    update_members = update.unboxed_update.updateMessage
                    assert_that(update_members.group_id, equal_to(new_group.group.id))
                    assert_that(update_members.members_count, equal_to(1))
                    break

    @allure.title("Test User1 update counter of members")
    def test_leave_user1_update_counter(self, d_user, _group, update1):
        updates1 = update1
        new_group = _group
        with allure.step('User1 gets update about changing group members count'):
            for update in updates1:
                print(update)
                if update.unboxed_update.HasField('updateGroupMembersCountChanged'):
                    update_members = update.unboxed_update.updateGroupMembersCountChanged
                    assert_that(update_members.group_id, equal_to(new_group.group.id))
                    assert_that(update_members.members_count, equal_to(1))
                    break

    @allure.title("Test User2 update counter of members")
    def test_leave_user2_update_counter(self, d_user, _group, update2):
        updates2 = update2
        new_group = _group
        with allure.step('User2 gets update about changing group members count'):
            for update in updates2:
                if update.unboxed_update.HasField('updateGroupMembersCountChanged'):
                    update_members = update.unboxed_update.updateGroupMembersCountChanged
                    assert_that(update_members.group_id, equal_to(new_group.group.id))
                    assert_that(update_members.members_count, equal_to(1))
                    break
