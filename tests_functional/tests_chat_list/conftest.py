import pytest
from dialog_api.groups_pb2 import GROUPTYPE_GROUP
from dialog_api.peers_pb2 import OutPeer


@pytest.fixture(scope="class")
def groups(d_user):
    """
    fixture for chat list test
    :param d_user: user
    :return: group conversation and p2p conversation with 2 messages
    """

    group1 = d_user.create_group(d_user.u1,
                                 user_outpeers=[d_user.outpeer1, d_user.outpeer5],
                                 group_type=GROUPTYPE_GROUP,
                                 with_shortname=True)
    d_user.send(d_user.u1,
                target_outpeer=OutPeer(id=group1.group.id, access_hash=group1.group.access_hash, type=2),
                num=2)
    for i in range(0, 2):
        d_user.send(d_user.u1, d_user.outpeer1)
    d_user.dialog_difference(d_user.u1)
    print(groups)
    yield groups
