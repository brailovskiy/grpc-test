import allure
from hamcrest import *
import pytest
from dialog_api.peers_pb2 import OutPeer


@allure.issue("SAN-13", "Reaction in channels")
@pytest.mark.incremental
@pytest.mark.usefixtures("d_user", "channel_reactons", "update1", "update2", "update3")
@pytest.mark.parametrize('d_user', ["3 users"], indirect=True)
class TestReactionChannel:
    """ Tests for setting reaction on message in channel """

    @allure.title("Test set reaction in channel")
    @allure.testcase("XTE-429", "Test set reaction in channel")
    def test_set_reaction_channel(self, d_user, channel_reactons, update1, update2, update3):
        """ Test same reaction in channel
        """
        group = channel_reactons[0]
        msg = channel_reactons[1]
        outpeer = OutPeer(id=group.group.id, access_hash=group.group.access_hash, type=2)
        code1 = ':thumbs_up:'
        with allure.step('User 2 set reaction to second message'):
            mid = msg[1].message_id
            reaction = d_user.set_reaction(d_user.u2, outpeer=outpeer, mid=mid, code=code1)
            set_emoji = reaction.reactions[0].code.encode('utf-8').decode('utf-8')
            print(set_emoji)
        with allure.step('All users load their history'):
            hist3 = d_user.load_history(d_user.u3, outpeer=outpeer)
            hist2 = d_user.load_history(d_user.u2, outpeer=outpeer)
            hist1 = d_user.load_history(d_user.u1, outpeer=outpeer)
            emoji1 = hist1.history[0].reactions[0].code.encode('utf-8').decode('utf-8')
            emoji2 = hist2.history[1].reactions[0].code.encode('utf-8').decode('utf-8')
            emoji3 = hist3.history[1].reactions[0].code.encode('utf-8').decode('utf-8')
        with allure.step('Reaction of all users shown in their message history are equal to sent'):
            assert_that(set_emoji, equal_to(emoji1) and equal_to(emoji2) and equal_to(emoji3))

    @allure.title("User1 get update for reaction in channel")
    def test_user1_get_update(self, update1, channel_reactons, d_user):
        updates1 = update1
        group = channel_reactons[0]
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

    @allure.title("User2 get update for reaction in channel")
    def test_user2_get_update(self, update2, channel_reactons, d_user):
        updates2 = update2
        group = channel_reactons[0]
        outpeer = OutPeer(id=group.group.id, access_hash=group.group.access_hash, type=2)
        hist2 = d_user.load_history(d_user.u2, outpeer=outpeer)
        print(hist2)
        emoji2 = hist2.history[1].reactions[0].code.encode('utf-8').decode('utf-8')
        with allure.step('User 2 update for reaction'):
            for update in updates2:
                print(update)
                if update.unboxed_update.HasField('updateReactionsUpdate'):
                    reaction = update.unboxed_update.updateReactionsUpdate
                    assert_that(reaction.peer.id, equal_to(group.group.id))
                    assert_that(reaction.reactions[-1].code.encode('utf-8').decode('utf-8'), equal_to(emoji2))
                    break

    @allure.title("User3 get update for reaction in channel")
    def test_user3_get_update(self, update3, channel_reactons, d_user):
        updates3 = update3
        group = channel_reactons[0]
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


    @allure.title("Test count different reactions in channel")
    @allure.testcase("XTE-431", "Test count different reactions in channel")
    def test_counter_reactions_channel(self, d_user, group_reactons, update1):
        """ Test count different reactions in channel"""
        updates1 = update1
        group = group_reactons[0]
        msg = group_reactons[1]
        outpeer = OutPeer(id=group.group.id, access_hash=group.group.access_hash, type=2)
        with allure.step('User 2 set reaction to second message'):
            mid = msg[1].message_id
            reaction = d_user.set_reaction(d_user.u2, outpeer=outpeer, mid=mid, code=None)
            set_emoji = reaction.reactions[0].code.encode('utf-8').decode('utf-8')
            print(set_emoji)
        with allure.step('User 1 and User 3 set reactions'):
            first_r = reaction.reactions[0]
            reaction2 = d_user.set_reaction(d_user.u3, outpeer=outpeer, mid=mid, code=None)
            second_r = reaction2.reactions[0]
            reaction3 = d_user.set_reaction(d_user.u1, outpeer=outpeer, mid=mid, code=None)
            third_r = reaction3.reactions[0]
        with allure.step('All reactions shows in update'):
            for update in updates1:
                reaction = update.unboxed_update.updateReactionsUpdate.reactions
                if len(reaction) >= 3:
                    reaction = [item.code for item in reaction]
                    assert_that(reaction, has_items(first_r.code, second_r.code, third_r.code))
                    break
