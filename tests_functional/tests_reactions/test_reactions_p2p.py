import allure
from hamcrest import *
import pytest


@allure.issue("SAN-13", "Reaction in peer to peer")
@pytest.mark.incremental
@pytest.mark.usefixtures("d_user", "update1", "update2")
@pytest.mark.parametrize('d_user', ["2 users"], indirect=True)
class TestReactionPrivate(object):
    """ Tests for setting reaction on message in p2p conversation """

    @allure.title("Test for reaction in p2p conversation")
    @allure.testcase("XTE-433", "Test for reaction in p2p conversation")
    def test_set_reaction_p2p(self, d_user, update1, update2):
        """ Test for set reaction in p2p conversation
        """
        with allure.step('User 1 send to user 2 3 messages'):
            msg = d_user.send(d_user.u1, d_user.outpeer1)
        with allure.step('User 2 set reaction to second message'):
            mid = msg[1].message_id
            reaction = d_user.set_reaction(d_user.u2, d_user.outpeer2, mid=mid, code=None)
            emoji = reaction.reactions[0].code.encode('utf-8').decode('utf-8')
            print(emoji)
        with allure.step('Both users load their history'):
            hist_rec = d_user.load_history(d_user.u2, d_user.outpeer2)
            hist_send = d_user.load_history(d_user.u1, d_user.outpeer1)
            print(hist_send)
            emoji_send = hist_send.history[0].reactions[0].code.encode('utf-8').decode('utf-8')
            emoji_rec = hist_rec.history[0].reactions[0].code.encode('utf-8').decode('utf-8')
        with allure.step('Reaction of both users shown in their message history'):
            assert_that(emoji, equal_to(emoji_send), equal_to(emoji_rec))

    def test_user1_update_for_reaction(self, d_user, update1):
        updates1 = update1
        with allure.step('User1 load message history'):
            hist_send = d_user.load_history(d_user.u1, d_user.outpeer1)
            emoji_send = hist_send.history[0].reactions[0].code.encode('utf-8').decode('utf-8')
        with allure.step('User 1 update for reaction'):
            for update in updates1:
                if update.unboxed_update.HasField('updateReactionsUpdate'):
                    reaction = update.unboxed_update.updateReactionsUpdate
                    assert_that(reaction.peer.id, equal_to(d_user.outpeer1.id))
                    assert_that(reaction.reactions[-1].code.encode('utf-8').decode('utf-8'), equal_to(emoji_send))
                    break

    def test_user2_update_for_reaction(self, d_user, update2):
        hist_rec = d_user.load_history(d_user.u2, d_user.outpeer2)
        emoji_rec = hist_rec.history[0].reactions[0].code.encode('utf-8').decode('utf-8')
        with allure.step('User 2 update for reaction'):
            updates2 = update2
            for update in updates2:
                if update.unboxed_update.HasField('updateReactionsUpdate'):
                    reaction = update.unboxed_update.updateReactionsUpdate
                    assert_that(reaction.peer.id, equal_to(d_user.outpeer2.id))
                    assert_that(reaction.reactions[-1].code.encode('utf-8').decode('utf-8'), equal_to(emoji_rec))
                    break


@pytest.mark.incremental
@pytest.mark.usefixtures("d_user", "update1", "update2")
@pytest.mark.parametrize('d_user', ["2 users"], indirect=True)
class TestReactionPrivate(object):
    @allure.title("Test for remove reaction in p2p conversation")
    @allure.testcase("XTE-432", "Test for remove reaction in p2p conversation")
    def test_remove_reaction_p2p(self, d_user, update1, update2):
        """ Test for remove reaction in p2p conversation
        """
        updates1 = update1
        list_msg = []
        with allure.step('User 1 send to user 2 3 messages'):
            for i in range(0, 3):
                msg = d_user.send(d_user.u1, d_user.outpeer1)
                list_msg.append(msg[1])
        with allure.step('User 2 set reaction to second message'):
            mid = list_msg[1].message_id
            code = ':thumbs_up:'
            reaction = d_user.set_reaction(d_user.u2, d_user.outpeer2, mid=mid, code=code)
            emoji = reaction.reactions[0].code.encode('utf-8').decode('utf-8')
        with allure.step('Reaction of user should show in message history'):
            for update in updates1:
                if update.unboxed_update.HasField('updateReactionsUpdate'):
                    reaction = update.unboxed_update.updateReactionsUpdate
                    print(reaction)
                    assert_that(reaction.peer.id, equal_to(d_user.outpeer1.id))
                    assert_that(reaction.reactions[-1].code.encode('utf-8').decode('utf-8'), equal_to(emoji))
                    break
        with allure.step('User2 remove reaction'):
            d_user.remove_reaction(d_user.u2, d_user.outpeer2, mid=mid, code=code)

    @allure.title("Test User2 update for remove reaction")
    def test_user2_update_for_delete_reaction(self, d_user, update2):
        updates2 = update2
        list_update = []
        with allure.step('User2 get update for deleted reaction'):
            for update in updates2:
                if update.unboxed_update.HasField('updateReactionsUpdate'):
                    list_update.append(update)
                    if len(list_update) >= 2:
                        break
            reaction = list_update[-1]
            assert_that(reaction.unboxed_update.updateReactionsUpdate.peer.id, equal_to(d_user.outpeer2.id))
            assert_that(len(reaction.unboxed_update.updateReactionsUpdate.reactions), equal_to(0))

    @allure.title("Test reaction removed from history")
    def test_reaction_removed_from_history(self, d_user):
        with allure.step('Both users load their history'):
            hist_send = d_user.load_history(d_user.u1, d_user.outpeer1)
            hist_rec = d_user.load_history(d_user.u2, d_user.outpeer2)
        with allure.step('Reaction of both users should not shown in their message history'):
            assert_that(len(hist_send.history[1].reactions), equal_to(0))
            assert_that(len(hist_rec.history[1].reactions), equal_to(0))
