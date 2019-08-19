import allure
import pytest
from hamcrest import *

from shared.constants import DefaultValues as DV

@pytest.mark.incremental
@pytest.mark.usefixtures("d_user", "update1", "clean_up")
@pytest.mark.parametrize('d_user', ["2 users"], indirect=True)
class TestEditUserProfile(object):
    """ Tests update data private profile"""

    @allure.title("Test User1 edit profile")
    def test_edit_avatar_in_private_profile(self, d_user, update1, clean_up):
        """ Test edit avatar in private profile """
        updates1 = update1
        with allure.step('User_1 edit avatar in his profile'):
            size = DV.jpg.stat().st_size
            expected_hash = d_user.hasher(file=DV.jpg)
            d_user.edit_avatar_profile(d_user.u1, DV.jpg)
        with allure.step('User_1 get update UpdateUser with new avatar'):
            for update in updates1:
                if update.unboxed_update.HasField('updateUser'):
                    data_update = update.unboxed_update.updateUser
                    assert_that(data_update.id, equal_to(d_user.u1.user_info.user.id))
                    assert_that(data_update.data.avatar.full_image.file_size, equal_to(size))
                    break
        with allure.step('Avatar updated'):
            users = d_user.load_user_data(d_user.u2).users
            user1 = list(filter(lambda x: x.id == d_user.u1.user_info.user.id, users))[0]
            d_user.download_file_by_file_location(d_user.u1, user1.data.avatar.full_image.file_location)
            f_hash = d_user.hasher(DV.jpg_loaded)
            assert_that(user1.data.avatar.full_image.file_size, equal_to(size))
            assert_that(f_hash, equal_to(expected_hash))

    @allure.title("Test User1 remove avatar from profile")
    def test_remove_avatar_in_private_profile(self, d_user, update1):
        """ Test remove avatar in private profile """
        updates1 = update1
        with allure.step('User_1 remove avatar in his profile'):
            d_user.remove_avatar_profile(d_user.u1)
        with allure.step('User_1 get update UpdateUser with deleted avatar'):
            for update in updates1:
                if update.unboxed_update.HasField('updateUser'):
                    data_update = update.unboxed_update.updateUser
                    assert_that(data_update.id, equal_to(d_user.u1.user_info.user.id))
                    assert_that(0, equal_to(data_update.data.avatar.full_image.file_size))
                    break
        with allure.step('Avatar deleted'):
            users = d_user.load_user_data(d_user.u2).users
            print(users)
            user1 = list(filter(lambda x: x.id == d_user.u1.user_info.user.id, users))[0]
            assert_that(user1.data.avatar.full_image.file_size, equal_to(0))
