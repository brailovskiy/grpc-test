import os

import allure
import pytest
from hamcrest import assert_that, equal_to

from shared.constants import DefaultValues as DV

# NEEDS REWORK ( hash calculating is incorrect )



@allure.issue("SAN-31", "File Sharing")
@pytest.mark.parametrize('d_user', ["2 users"], indirect=True)
class TestFileMessage:
    """ Tests for uploading and sharing files """

    @allure.title("Test for uploading txt document")
    @allure.testcase("XTE-17", "Test for uploading txt document")
    def test_send_txt_file(self, d_user, gen_txt, clean_up_txt):
        """ Test for uploading txt document
        """
        with allure.step('Check hashsum before uploading'):
            sended_sum = d_user.hasher(file=DV.txt)
        with allure.step('User1 uploads file'):
            d_user.send_file(d_user.u1, d_user.outpeer1, file=DV.txt)
        with allure.step('User2 download file'):
            d_user.download(d_user.u2, d_user.outpeer2)
        with allure.step('Check hashsum after uploading'):
            loaded_sum = d_user.hasher(file=DV.txt_loaded)
        with allure.step('Check files extension'):
            name, ext = os.path.splitext(DV.txt)
            name_loaded, ext_loaded = os.path.splitext(DV.txt_loaded)
        with allure.step('Hashsums and extensions are equal'):
            assert_that(sended_sum, equal_to(loaded_sum))
            assert_that(ext, equal_to(ext_loaded))

    def test_share_txt_file(self, d_user, gen_txt, clean_up_txt):
        """ Test for sharing txt document
        """
        with allure.step('Check hashsum before uploading'):
            sended_sum = d_user.hasher(file=DV.txt)
        with allure.step('User1 share file'):
            d_user.share_file(d_user.u1, d_user.outpeer1, file=DV.txt)
        with allure.step('User2 download file'):
            d_user.download(d_user.u2, d_user.outpeer2)
        with allure.step('Check hashsum after sharing'):
            loaded_sum = d_user.hasher(file=DV.txt_loaded)
        with allure.step('Check files extension'):
            name, ext = os.path.splitext(DV.txt)
            name_loaded, ext_loaded = os.path.splitext(DV.txt_loaded)
        with allure.step('Hashsums and extensions are equal'):
            assert_that(sended_sum, equal_to(loaded_sum))
            assert_that(ext, equal_to(ext_loaded))
