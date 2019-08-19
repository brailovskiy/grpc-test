import allure
import pytest
from hamcrest import *


@allure.issue("SAN-41", "Create Channels")
@pytest.mark.parametrize('d_user', ["3 users"], indirect=True)
class TestCreateChannels:
    """ Tests for creating channels """

    @allure.title("Test create channel with member")
    @allure.testcase("XTE-41", "Test create channel with member")
    def test_create_channel(self, d_user, update2, _channel):
        """  Create channel with member"""
        updates = update2
        with allure.step('User1 create channnel with User2'):
            new_channel = _channel
            channel = new_channel.group
        with allure.step('Usder2 gets update for inviting to channel'):
            for update in updates:
                if update.unboxed_update.HasField('updateGroupInviteObsolete'):
                    assert_that(update.unboxed_update.updateGroupInviteObsolete.group_id == channel.id)
                    break
        with allure.step('User2 have created channel in chat list'):
            chats, chats_id = d_user.load_dialogs_with_wait(d_user.u2, channel.id)
            assert_that(chats_id, has_item(channel.id))

    @allure.title("Test searching public channel by not a member of channel")
    @allure.testcase("XTE-43", "Test searching public channel by not a member of channel")
    def test_search_channel(self, _channel, d_user):
        """  Searching public channel by not a member of channel"""
        channel = _channel.group
        with allure.step('User3 search channel created in previous test'):
            search_results = d_user.search_peers(
                user=d_user.u3, query=channel.title, search_type=['group', 'contact', 'public'])
            print("\tSearch results: ")
            print(search_results)
            assert_that([(i.peer.id, i.title, i.peer.type) for i in search_results.search_results],
                        has_item((channel.id, channel.title, channel.group_type)))

    @allure.title("Test add member to channel")
    @allure.testcase("XTE-25", "Test add member to channel")
    def test_add_member_to_channel(self, d_user, update3, _channel):
        """  Inviting user to public channel """
        updates = update3
        channel = _channel.group
        with allure.step('User1 invite User3 to channel^ created before'):
            d_user.add_group_members(d_user.u1, d_user.outpeer5, channel)
        with allure.step('User3 gets update for inviting to channel'):
            for update in updates:
                if update.unboxed_update.HasField('updateGroupInviteObsolete'):
                    assert_that(update.unboxed_update.updateGroupInviteObsolete.group_id == channel.id)
                    break
        with allure.step('User3 have channel in chat list'):
            chats, chats_id = d_user.load_dialogs_with_wait(d_user.u3, channel.id)
            assert_that(chats_id, has_item(channel.id))
