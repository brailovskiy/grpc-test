import pytest


@pytest.fixture(scope='class')
def leave_group(d_user, _group):
    new_group = _group
    yield d_user.leave_group(d_user.u2, new_group.group)
