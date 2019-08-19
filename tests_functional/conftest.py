import pytest
from dialog_api.groups_pb2 import GROUPTYPE_GROUP, GROUPTYPE_CHANNEL
from google.protobuf import empty_pb2
from sdk_testing_framework.messaging import Messaging
from shared.data_generators import Generators
import os
import shutil
from shared.constants import DefaultValues as DV


@pytest.fixture(scope="class")
def d_user(users_gen, users_real_gen, cmdopt, request):
    """
    Initializing object for pre-defining tests:
    Got two args for choice needed type of users
    ( generate dummy users or using users with real authorization with password and login )
    Quantity of needed users setiing in pytest decorator
    @pytest.mark.parametrize('d_user', [(val)], indirect=True)
    where val - quantity of users. !!! Note max number of users 3
    """
    global users_num
    if request.param == "2 users":
        users_num = 2
    elif request.param == "3 users":
        users_num = 3
    if cmdopt == 'type1':
        print("\n*** START test session with %s dummy-generated users ***" % users_num)
        yield Messaging(users_gen, users_num)
        print("\n*** END test session ***")
    elif cmdopt == 'type2':
        print("\n*** START test session with %s pre-defined users ***" % users_num)
        yield Messaging(users_real_gen, users_num, real_users=True)
        print("\n*** END test session ***")


@pytest.fixture(autouse=True)
def any_custom_setup():
    """ Text status for readability """
    print("*** SETUP COMPLITE ***")


@pytest.fixture(scope='class')
def update1(d_user):
    """ Pre-condition: 'User1 calls seq updates' """
    yield d_user.u1.updates.SeqUpdates(empty_pb2.Empty())


@pytest.fixture(scope='class')
def update2(d_user):
    """ Pre-condition: 'User2 calls seq updates' """
    yield d_user.u2.updates.SeqUpdates(empty_pb2.Empty())


@pytest.fixture(scope='class')
def update3(d_user):
    """ Pre-condition: 'User3 calls seq updates' """
    yield d_user.u3.updates.SeqUpdates(empty_pb2.Empty())


@pytest.fixture(scope='class', autouse=True)
def send_message(d_user):
    """ Pre-condition: 'User1 send one text message to User2' """
    d_user.send(d_user.u1, d_user.outpeer1)


@pytest.fixture(scope='class')
def _channel(d_user):
    """ Pre-condition: 'User1 create channel with User2' """
    yield d_user.create_group(d_user.u1, [d_user.outpeer1], GROUPTYPE_CHANNEL, with_shortname=True)


@pytest.fixture(scope='class')
def _group(d_user):
    """ Pre-condition: 'User1 create group with User2' """
    yield d_user.create_group(d_user.u1, [d_user.outpeer1], GROUPTYPE_GROUP, with_shortname=True)


@pytest.fixture(scope="class")
def gen_txt():
    """ Pre-condition: generate 5mb txt file """
    yield Generators.random_txt_file()


@pytest.fixture(scope="class")
def clean_up_txt():
    """ Post-condition: clean txt file """
    yield
    if os.path.exists(DV.txt):
        os.remove(DV.txt)
    else:
        print("Nothing to clean")


@pytest.fixture(scope="function", autouse=True)
def clean_up():
    """ Workspace: create tmp directory for file sharing&uploading tests
        Remove directory after test session
    """
    if not os.path.exists(DV.downloads):
        os.makedirs(DV.downloads)
    yield
    if os.path.exists(DV.downloads):
        shutil.rmtree(DV.downloads)
