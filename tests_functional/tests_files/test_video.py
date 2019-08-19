import os

import allure
import pytest
from hamcrest import assert_that, equal_to
from shared.constants import DefaultValues as DV


@allure.issue("SAN-45", "Send Video")
@pytest.mark.parametrize('d_user', ["2 users"], indirect=True)
class TestVideoMessage:
    """ Tests for sending video """
    @allure.title("Test send video message")
    @allure.testcase("XTE-16","Test send video message")
    def test_send_video(self, d_user):
        """ Test send video message
        """
        with allure.step('Check hashsum before uploading'):
            sended_sum = d_user.hasher(file=DV.video)
        with allure.step('User1 send video'):
            d_user.send_video(d_user.u1, d_user.outpeer1, file=DV.video)
        with allure.step('User2 load video'):
            d_user.download(d_user.u2, d_user.outpeer2)
        with allure.step('User2 loads history. Counting hash sum after upload'):
            hist = d_user.load_history(d_user.u2, d_user.outpeer2)
            loaded_sum = d_user.hasher(file=DV.video_loaded)
        with allure.step('Loaded file showing as video and has video field extension'):
            assert_that(hist.history[0].message.documentMessage.ext.video is not None)
        with allure.step('Check files extension'):
            name, ext = os.path.splitext(DV.video)
            name_loaded, ext_loaded = os.path.splitext(DV.video_loaded)
        with allure.step('Hashsums and extensions are equal'):
            assert_that(sended_sum, equal_to(loaded_sum))
            assert_that(ext, equal_to(ext_loaded))

    def test_share_video(self, d_user):
        """ Test for sharing image
        """
        with allure.step('Check hashsum before uploading'):
            sended_sum = d_user.hasher(file=DV.video)
        with allure.step('User1 share file'):
            d_user.share_file(d_user.u1, d_user.outpeer1, file=DV.video)
        with allure.step('User2 load video'):
            d_user.download(d_user.u2, d_user.outpeer2)
        with allure.step('Check hashsum after sharing'):
            loaded_sum = d_user.hasher(file=DV.video_loaded)
        with allure.step('Check files extension'):
            name, ext = os.path.splitext(DV.video)
            name_loaded, ext_loaded = os.path.splitext(DV.video_loaded)
        with allure.step('Hashsums and extensions are equal'):
            assert_that(sended_sum, equal_to(loaded_sum))
            assert_that(ext, equal_to(ext_loaded))
