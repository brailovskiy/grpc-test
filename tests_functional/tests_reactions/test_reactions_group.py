import allure
from hamcrest import *
import pytest
from dialog_api.peers_pb2 import OutPeer


@allure.issue("SAN-13", "Reaction in group")


@pytest.mark.incremental
@pytest.mark.usefixtures("d_user", "update1", "update2", "update3", "group_reactons")
@pytest.mark.parametrize('d_user', ["3 users"], indirect=True)
class TestReactionGroupUpdates(object):
    """ Tests for setting reaction on message in group chat """
    @allure.title("Reaction in group chat")
    @allure.testcase("XTE-430", "Test for reaction in group chat")
    def test_set_reaction_group(self, d_user, group_reactons):
        """ Test for reaction in group chat
        """
        group = group_reactons[0]
        msg = group_reactons[1]
        outpeer = OutPeer(id=group.group.id, access_hash=group.group.access_hash, type=2)
        with allure.step('User 2 set reaction to second message'):
            mid = msg[1].message_id
            reaction = d_user.set_reaction(d_user.u2, outpeer=outpeer, mid=mid, code=':thumbs_up:')
            emoji = reaction.reactions[0].code.encode('utf-8').decode('utf-8')
            print(emoji)

    @allure.title("User1 update for reaction in group")
    def test_user1_updates(self, d_user, update1, group_reactons):
        updates1 = update1
        group = group_reactons[0]
        outpeer = OutPeer(id=group.group.id, access_hash=group.group.access_hash, type=2)
        hist1 = d_user.load_history(d_user.u1, outpeer=outpeer)
        emoji1 = hist1.history[0].reactions[0].code.encode('utf-8').decode('utf-8')
        with allure.step('User 1 update for reaction'):
            for update in updates1:
                if update.unboxed_update.HasField('updateReactionsUpdate'):
                    reaction = update.unboxed_update.updateReactionsUpdate
                    assert_that(reaction.peer.id, equal_to(group.group.id))
                    assert_that(reaction.reactions[-1].code.encode('utf-8').decode('utf-8'), equal_to(emoji1))
                    break

    @allure.title("User2 update for reaction in group")
    def test_user2_updates(self, d_user, update2, group_reactons):
        updates2 = update2
        group = group_reactons[0]
        outpeer = OutPeer(id=group.group.id, access_hash=group.group.access_hash, type=2)
        hist2 = d_user.load_history(d_user.u2, outpeer=outpeer)
        emoji2 = hist2.history[1].reactions[0].code.encode('utf-8').decode('utf-8')
        with allure.step('User 2 update for reaction'):
            for update in updates2:
                print(update)
                if update.unboxed_update.HasField('updateReactionsUpdate'):
                    reaction = update.unboxed_update.updateReactionsUpdate
                    assert_that(reaction.peer.id, equal_to(group.group.id))
                    assert_that(reaction.reactions[-1].code.encode('utf-8').decode('utf-8'), equal_to(emoji2))
                    break

    @allure.title("User3 update for reaction in group")
    def test_user3_updates(self, d_user, update3, group_reactons):
        updates3 = update3
        group = group_reactons[0]
        outpeer = OutPeer(id=group.group.id, access_hash=group.group.access_hash, type=2)
        hist3 = d_user.load_history(d_user.u3, outpeer=outpeer)
        print(hist3)
        emoji3 = hist3.history[1].reactions[0].code.encode('utf-8').decode('utf-8')
        with allure.step('User 3 update for reaction'):
            for update in updates3:
                print(update)
                if update.unboxed_update.HasField('updateReactionsUpdate'):
                    reaction = update.unboxed_update.updateReactionsUpdate
                    assert_that(reaction.peer.id, equal_to(group.group.id))
                    assert_that(reaction.reactions[-1].code.encode('utf-8').decode('utf-8'), equal_to(emoji3))
                    break

@pytest.mark.incremental
@pytest.mark.usefixtures("d_user", "update1", "group_reactons")
@pytest.mark.parametrize('d_user', ["3 users"], indirect=True)
class TestSameReactionInGroup(object):
    @allure.title("Test count for same reaction in group chat")
    @allure.testcase("XTE-434", "Test count for same reaction in group chat")
    def test_users_same_reaction_group(self, d_user, group_reactons, update1):
        """ Test count for same reaction in group chat
        """
        updates1 = update1
        group = group_reactons[0]
        msg = group_reactons[1]
        outpeer = OutPeer(id=group.group.id, access_hash=group.group.access_hash, type=2)
        list_update = []
        with allure.step('User 2 set reaction to second message'):
            mid = msg[1].message_id
            reaction = d_user.set_reaction(d_user.u2, outpeer=outpeer, mid=mid, code=':thumbs_up:')
            emoji = reaction.reactions[0].code.encode('utf-8').decode('utf-8')
            print(emoji)
        with allure.step('User 3 set same reaction'):
            d_user.set_reaction(d_user.u3, outpeer=outpeer, mid=mid, code=':thumbs_up:')
        with allure.step('Counter of reacted user increased to 2 and reacted users listed in update'):
            for update in updates1:
                if update.unboxed_update.HasField('updateReactionsUpdate'):
                    list_update.append(update)
                    reacted_users = update.unboxed_update.updateReactionsUpdate.reactions[0]
                    if len(reacted_users.users) == 2:
                        assert_that(reacted_users.users, has_items(d_user.outpeer1.id, d_user.outpeer5.id))
                        break
