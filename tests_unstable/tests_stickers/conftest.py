import pytest

from shared import dashboard_helpers
from shared.data_generators import Generators


@pytest.fixture(scope='function')
def load_stickers(d_user):
    """ Loading stickerpack """
    load_sticker = d_user.load_stickers(d_user.u1)
    print("count of loaded sticker-packs: %s" % len(load_sticker.accessible_stickers))
    yield load_sticker

@pytest.fixture(scope='function')
def create_stickerpack(d_user):
    "Admin create new stickerpack and set it shared"
    stickerpack = dashboard_helpers.AdminTools().make_graphql_request(
        dashboard_helpers.mutation_create(user_id=d_user.u1.user_info.user.id, title=Generators.random_stickerpack()))
    stickerpack_id = int(stickerpack['data']['stickers_create_pack'][1:-1].split(',')[0])
    dashboard_helpers.AdminTools().make_graphql_request(dashboard_helpers.mutation_set_share(pack_id=stickerpack_id))
    return stickerpack_id