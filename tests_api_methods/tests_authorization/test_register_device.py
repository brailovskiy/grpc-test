import allure
from hamcrest import assert_that, equal_to

from tests_api_methods.authorizattion import Authorize


@allure.issue("SAN-3", "login & password authorization")
class TestRegistration:
    """ Tests for device registration
    """

    @allure.title("Test max app_id")
    @allure.testcase("XTR-307")
    def test_auth_max_int32(self):
        """
        Should authenticate with max app_id field
        """
        app_id = 2147483647
        with allure.step("Request session"):
            auth = Authorize().get_session_token(app_id_filled=app_id)
            assert_that(hasattr(auth, 'token') is True)

    @allure.title("Test min app_id")
    @allure.testcase("XTR-308")
    def test_auth_min_int32(self):
        """
        Should authenticate with mix app_id field
        """
        app_id = -2147483648
        with allure.step("Request session"):
            auth = Authorize().get_session_token(app_id_filled=app_id)
            assert_that(hasattr(auth, 'token') is True)

    @allure.title("Test bigger than int32")
    @allure.testcase("XTR-309")
    def test_auth_bigger_int32(self):
        """
        Should not authenticate with max app_id field
        """
        app_id = 2147483647+1
        with allure.step("Request session"):
            try:
                res = Authorize().get_session_token(app_id_filled=app_id)
                print(res)
            except ValueError as e:
                assert_that(str(e),  equal_to('Value out of range: 2147483648'))

    @allure.title("Test smaller then int32")
    @allure.testcase("XTR-312")
    def test_auth_smaller_int32(self):
        """
        Should not authenticate with mix app_id field
        """
        app_id = -2147483648-1
        with allure.step("Request session"):
            try:
                res = Authorize().get_session_token(app_id_filled=app_id)
                print(res)
            except ValueError as e:
                assert_that(str(e), equal_to('Value out of range: -2147483649'))

    @allure.title("Test null app id")
    @allure.testcase("XTR-313")
    def test_auth_null_app_id(self):
        """
        Should authenticate with null app_id field
        app_id=0 equal to app_id=None
        """
        app_id = 0
        with allure.step("Request session"):
            auth = Authorize().get_session_token(app_id_filled=app_id)
            assert_that(hasattr(auth, 'token') is True)