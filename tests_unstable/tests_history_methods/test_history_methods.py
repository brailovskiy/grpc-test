""" tests for load history
get some msg

tests for methods:
solid +
count after
slice
merge

"""

import allure
from hamcrest import *
from tests_unstable.tests_history_methods.history import *
import pytest


@allure.issue("History methods")
@pytest.mark.skip(reason="tests for local-defined methods")
class TestHistoryMethods:
    """ Tests for sdk_testing_framework/history.py """

    @allure.title("Test for solid")
    @allure.testcase("XTE-10", "Test for solid")
    def test_history_solid(self, d_user):
        """ Test is_solid """
        with allure.step('User1 and User2 send 5 messages each'):
            d_user.send(d_user.u1, d_user.outpeer1, 5)
            d_user.send(d_user.u2, d_user.outpeer2, 5)
        with allure.step('User1 load history'):
            history = d_user.load_history(d_user.u1, d_user.outpeer1)
        with allure.step('Check history is solid'):
            hist = HistoryData(history.history[0].date, 0, [HMessage(h.mid, h.date) for h in history.history])
            assert_that(hist.is_solid(), equal_to(True))

    @allure.title("Test for slice")
    @allure.testcase("XTE-34", "Test for slice")
    def test_history_slice(self, d_user):
        """ Test for slice - get part of history from to till of setted message """
        with allure.step('User1 and User2 send 5 messages each'):
            d_user.send(d_user.u1, d_user.outpeer1, 5)
            d_user.send(d_user.u2, d_user.outpeer2, 5)
        with allure.step('User1 load history'):
            history = d_user.load_history(d_user.u1, d_user.outpeer1)
        with allure.step('get history sliceк from 5 to last message'):
            hist = HistoryData(history.history[0].date, 0, [HMessage(h.mid, h.date) for h in history.history])
            sliced_hist = hist.slice(from_date=int(history.history[4].date), to_date=int(history.history[0].date))
        with allure.step('In sliced part listed 5 messages'):
            assert_that([m.date for m in sliced_hist.messages], has_length(5))

    @allure.title("Test for count after")
    @allure.testcase("XTE-12", "Test for count after")
    def test_history_count_after(self, d_user):
        """ test for count_after - count messages after chosen message to the end of list  """
        with allure.step('User1 and User2 send 5 messages each'):
            d_user.send(d_user.u1, d_user.outpeer1, 5)
            d_user.send(d_user.u2, d_user.outpeer2, 5)
        with allure.step('User1 load history'):
            history = d_user.load_history(d_user.u1, d_user.outpeer1)
        with allure.step('From 4 message to the end of list are 3 messages'):
            hist = HistoryData(history.history[0].date, 0, [HMessage(h.mid, h.date) for h in history.history])
            assert_that(hist.count_after(_from=int(history.history[3].date)), equal_to(3))

    @allure.title("Test for merge")
    @allure.testcase("XTE-32", "Test for merge")
    def test_history_merge(self, d_user):
        """ Test for merge method -  слияние двух кусков истории сообщений"""
        with allure.step('User1 and User2 send 5 messages each'):
            d_user.send(d_user.u1, d_user.outpeer1, 5)
            d_user.send(d_user.u2, d_user.outpeer2, 5)
        with allure.step('User1 load history'):
            history = d_user.load_history(d_user.u1, d_user.outpeer1)
            hist = HistoryData(history.history[0].date, 0, [HMessage(h.mid, h.date) for h in history.history])
        with allure.step('Take slice from 5 message to last'):
            sliced_hist_start = hist.slice(from_date=int(history.history[4].date), to_date=int(history.history[0].date))
        with allure.step('Take slice from 10 message to 5'):
            sliced_hist_end = hist.slice(from_date=int(history.history[9].date), to_date=int(history.history[4].date))
        with allure.step('Merge two slices'):
            merge = HistoryDataOps.merge(
                a=sliced_hist_start,
                b=sliced_hist_end)
        with allure.step('Merged history have 10 messages and solid'):
            assert_that([m.date for m in merge.messages], has_length(10))
            assert_that(merge.is_solid(), equal_to(True))

    @allure.title("Test for not solid")
    @allure.testcase("XTE-31", "Test for not solid")
    def test_history_not_solid(self, d_user):
        """ Test merge is not solid (negative case)"""
        with allure.step('User1 and User2 send 5 messages each'):
            d_user.send(d_user.u1, d_user.outpeer1, 5)
            d_user.send(d_user.u2, d_user.outpeer2, 5)
        with allure.step('User1 load history'):
            history = d_user.load_history(d_user.u1, d_user.outpeer1)
            hist = HistoryData(history.history[0].date, 0, [HMessage(h.mid, h.date) for h in history.history])
        with allure.step('Take slice from 4 message to last'):
            sliced_hist_start = hist.slice(from_date=int(history.history[3].date), to_date=int(history.history[1].date))
        with allure.step('Take slice from 9 message to 7'):
            sliced_hist_end = hist.slice(from_date=int(history.history[8].date), to_date=int(history.history[6].date))
            assert_that(hist.is_solid(), equal_to(True))
        with allure.step('Merge slices'):
            merge = HistoryDataOps.merge(
                a=sliced_hist_start,
                b=sliced_hist_end)
        with allure.step('History is not solid'):
            assert_that(merge.is_solid(), equal_to(False))
