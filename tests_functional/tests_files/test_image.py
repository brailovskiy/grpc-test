import os

from shared.constants import DefaultValues as DV
import allure
import pytest
from hamcrest import *

from shared.utils.get_image_metadata import get_image_thumb_bytes

# NEEDS REWORK ( hash calculating is incorrect )



@allure.issue("SAN-25", "Send Image")
@pytest.mark.parametrize('d_user', ["2 users"], indirect=True)
class TestImageMessage:
    """ Tests for sending image """

    @allure.title("Test send image")
    @allure.testcase("XTE-37", "Test send image")
    def test_send_image(self, d_user):
        """ Test send image
        """
        with allure.step('Check hashsum before uploading'):
            sended_sum = d_user.hasher(file=DV.gif)
        with allure.step('Getting thumb and counting hash'):
            thumb = get_image_thumb_bytes(file=DV.gif)
            thumb_h = bytes(thumb[2])
        with allure.step('User1 send image'):
            d_user.send_image(d_user.u1, d_user.outpeer1, file=DV.gif)
        with allure.step('User2 load image'):
            d_user.download(d_user.u2, d_user.outpeer2)
            name, ext = os.path.splitext(DV.gif_loaded)
            print(ext)
        with allure.step('User2 load history, check hashsum after uploading and count bytes of thumbnail'):
            hist = d_user.load_history(d_user.u2, d_user.outpeer2)
            loaded_sum = d_user.hasher(file=DV.gif_loaded)
            loaded_thumb = bytes(hist.history[0].message.documentMessage.thumb.thumb)
        with allure.step('Loaded file showing as image and has photo field extension'):
            print(hist.history[0].message.documentMessage.ext)
            assert_that(hist.history[0].message.documentMessage.ext.photo is not None)
        with allure.step('Check files extension'):
            name, ext = os.path.splitext(DV.gif)
            name_loaded, ext_loaded = os.path.splitext(DV.gif_loaded)
        with allure.step('Checking hashes, extensions and thumbs'):
            assert_that(sended_sum, equal_to(loaded_sum))
            assert_that(ext, equal_to(ext_loaded))
            assert_that(thumb_h, equal_to(loaded_thumb))

    def test_share_image(self, d_user):
        """ Test for sharing image
        """
        with allure.step('Check hashsum before uploading'):
            sended_sum = d_user.hasher(file=DV.gif)
        with allure.step('User1 share image'):
            d_user.share_file(d_user.u1, d_user.outpeer1, file=DV.gif)
        with allure.step('User2 load image'):
            d_user.download(d_user.u2, d_user.outpeer2)
        with allure.step('Check hashsum after sharing'):
            loaded_sum = d_user.hasher(file=DV.gif_loaded)
        with allure.step('Check files extension'):
            name, ext = os.path.splitext(DV.gif)
            name_loaded, ext_loaded = os.path.splitext(DV.gif_loaded)
        with allure.step('Hashes are equal'):
            assert_that(ext, equal_to(ext_loaded))
            assert_that(sended_sum, equal_to(loaded_sum))