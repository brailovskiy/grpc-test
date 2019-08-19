import pytest
import os
import logging
import allure

from sdk_testing_framework import users


def pytest_addoption(parser):
    parser.addoption(
        "--auth", action="store", default="type2", help='type1 - use dummy users, type2 - use pre-defined users '
    )

    parser.addoption(
        "--ep", action="store", default="stand-1.transmit.im", help='select pre-defined or custom endpoint'
    )



def pytest_configure(config):
    ep = config.getoption('--ep')
    print("******************")

    print('using custom endpoint...')
    os.environ["endpoint"] = ep + ":9443"
    os.environ['SHARING_URL'] = "https://" + ep + ":443"
    os.environ["auth_url"] = "https://" + ep + "/api/v1/admin/auth"
    os.environ["graph_url"] = "https://" + ep + "/api/v1/admin/graph"
    print(os.environ["endpoint"])


@pytest.fixture(scope="session")
def cmdopt(request):
    return request.config.getoption("--auth")


@pytest.fixture(scope="module")
def users_gen():
    """User generator"""

    def _user():
        print("preparing user...")
        return users.Users().get_user()

    yield _user


@pytest.fixture(scope="module")
def users_real_gen():
    """Logo&pass user generator"""
    os.environ["user1_login"] = 'tester1'
    os.environ["user2_login"] = 'tester2'
    os.environ["user3_login"] = 'tester3'
    os.environ["user4_login"] = 'tester4'
    os.environ["user5_login"] = 'tester5'
    password = os.getenv('password')
    

    def _user(login):
        print("preparing user...")
        return users.Users().get_real_user(login, password)

    yield _user


def pytest_runtest_makereport(item, call):
    if "incremental" in item.keywords:
        if call.excinfo is not None:
            parent = item.parent
            parent._previousfailed = item


def pytest_runtest_setup(item):
    if "incremental" in item.keywords:
        previousfailed = getattr(item.parent, "_previousfailed", None)
        if previousfailed is not None:
            pytest.xfail("previous test failed (%s)" % previousfailed.name)


# @pytest.fixture(scope="session", autouse=True)
# def write_allure_env():
#     """ Write environment to alluredir """
#     yield
#
#
# class AllureLoggingHandler(logging.Handler):
#     def log(self, message):
#         with allure.step('Log {}'.format(message)):
#             pass
#
#     def emit(self, record):
#         self.log("[{}] {}".format(record.levelname, record.getMessage()))
#
#
# class AllureCatchLogs:
#     def __init__(self):
#         self.rootlogger = logging.getLogger()
#         self.allurehandler = AllureLoggingHandler()
#
#     def __enter__(self):
#         if self.allurehandler not in self.rootlogger.handlers:
#             self.rootlogger.addHandler(self.allurehandler)
#
#     def __exit__(self, exc_type, exc_value, traceback):
#         self.rootlogger.removeHandler(self.allurehandler)
#
#
# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_setup():
#     with AllureCatchLogs():
#         yield
#
#
# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_call():
#     with AllureCatchLogs():
#         yield
#
#
# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_teardown():
#     with AllureCatchLogs():
#         yield



def pytest_collection_modifyitems(session, config, items):
    for item in items:
        for marker in item.iter_markers(name="Feature"):
            feature_key = marker.args[0]
            item.user_properties.append(("Feature", feature_key))
