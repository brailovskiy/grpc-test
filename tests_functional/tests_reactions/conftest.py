import time
import pytest

from dialog_api.groups_pb2 import GROUPTYPE_GROUP, GROUPTYPE_CHANNEL
from dialog_api.peers_pb2 import OutPeer


@pytest.fixture(scope="class")
def group_reactons(d_user):
    """ Pre-defined options: User 1 creates group with User 2 & User 3 and send one message"""
    group = d_user.create_group(d_user.u1,
                                user_outpeers=[d_user.outpeer1, d_user.outpeer5],
                                group_type=GROUPTYPE_GROUP,
                                with_shortname=True)
    msg = d_user.send(d_user.u1,
                      target_outpeer=OutPeer(id=group.group.id, access_hash=group.group.access_hash, type=2))
    d_user.dialog_difference(d_user.u1)
    yield group, msg


@pytest.fixture(scope="class")
def channel_reactons(d_user):
    """ Pre-defined options: User 1 creates channel with User 2 & User 3 and send one message"""
    channel = d_user.create_group(d_user.u1,
                                  user_outpeers=[d_user.outpeer1, d_user.outpeer5],
                                  group_type=GROUPTYPE_CHANNEL,
                                  with_shortname=True)
    ch_outpeer = OutPeer(id=channel.group.id, access_hash=channel.group.access_hash, type=2)
    msg = d_user.send(d_user.u1,
                      target_outpeer=ch_outpeer)
    d_user.dialog_difference(d_user.u1)

    # Triggering system message "User invited to the group"
    date = int(time.time())
    d_user.read_message(d_user.u2, outpeer=ch_outpeer, date=date)
    d_user.read_message(d_user.u3, outpeer=ch_outpeer, date=date)
    yield channel, msg
