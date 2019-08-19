from shared.data_generators import Generators
import allure
import pytest
from shared import dashboard_helpers, update_helpers


@allure.issue("SAN-14", "Stickers")
@pytest.mark.parametrize('d_user', ["2 users"], indirect=True)
class TestStickers:
    """Tests for stickers"""

    @allure.title("Test for upload stickers")
    @allure.testcase("XTE-39", "Test for upload stickers")
    def test_stickers_load(self, d_user, load_stickers):
        """Test for loadinng stickers and loading stickers difference"""
        load_sticker = load_stickers
        print(load_sticker)
        with allure.step('Sticker collection loaded and not empty'):
            assert len(load_sticker.accessible_stickers) > 0
            """ writing clock from answer"""
            saved_clock = load_sticker.clock
        with allure.step('User1 loading stickers with saved clock'):
            load_sticker2 = d_user.load_stickers(d_user.u1, saved_clock)
            print(load_sticker2)
        with allure.step('No new stickers with setted clock'):
            assert len(load_sticker2.accessible_stickers) == 0

    @allure.title("Test updates for sticker changed")
    @allure.testcase("XTE-24", "Test updates for sticker changed")
    @pytest.mark.xfail()
    def test_core(self, d_user, update1, load_stickers, create_stickerpack):
        """Test updates for changing stickers"""
        seq_updates = update1
        title = Generators.random_stickerpack()
        load_sticker = load_stickers
        stickerpack_id = create_stickerpack
        print(stickerpack_id)
        with allure.step("Admin change name of one sticker"):
            query = dashboard_helpers.mutation_set_title(pack_id=stickerpack_id, title=title)
            req = dashboard_helpers.AdminTools().make_graphql_request(query)
            print(req)
        with allure.step("User1 get seq update with updated sticker collection id"):
            for update in seq_updates:
                print(update)
                if update.unboxed_update.HasField("updateStickerCollectionsChanged"):
                    assert update.unboxed_update.updateStickerCollectionsChanged.updated_collections[0].id == stickerpack_id
                    break

    @allure.title("Test weak updates for stickers")
    @allure.testcase("XTE-14", "Test weak updates for stickers")
    @pytest.mark.xfail()
    def test_weak_stickers(self, d_user, load_stickers, create_stickerpack):
        """Weak updates for stickers
        """
        message = update_helpers.make_subscribe_to_onlines(d_user.outpeer1.id, d_user.outpeer1.access_hash)
        updates = update_helpers.UpdateHelpers.weak_updates_helper(d_user.u1.obsolete, message)
        title = Generators.random_stickerpack()
        load_sticker = load_stickers
        stickerpack_id = create_stickerpack
        with allure.step("Admin change name of sticker collection"):
            query = dashboard_helpers.mutation_set_title(pack_id=stickerpack_id, title=title)
            dashboard_helpers.AdminTools().make_graphql_request(query)
        with allure.step("User1 get weak update withn changed sticker collection id"):
            for update in updates:
                if update.update_any.HasField("updateStickerCollectionsChanged"):
                    print(update)
                    assert update.update_any.updateStickerCollectionsChanged.updated_collections[0].id == stickerpack_id
                    break
