import os

import allure
import grpc
from hamcrest import *
from shared.data_generators import Generators
from tests_api_methods.authorizattion import Authorize


@allure.issue("SAN-3", "login & password authorization")
class TestAuthorization:
    """ Tests for authorization with login and password
    """
    random_login = Generators.get_random_login()
    random_password = Generators.get_random_password()
    @allure.title("Test valid password, valid login")
    @allure.testcase("XTR-306")
    def test_succeful_authorize(self):
        """
        Succeful authorization
        """
        with allure.step("Make authorize"):
            login = 'tester1'
            pasword = os.getenv('password')
            auth = Authorize().username_authorize(login=login, password=pasword)
            assert_that(auth.user.data.name, equal_to(login))
            assert_that(auth.HasField('config'))
            assert_that(auth.HasField('config_hash'))

    @allure.title("Test invalid password, valid login")
    @allure.testcase("XTR-305")
    def test_inv_val(self):
        """
        Failed authorization
        """
        with allure.step("Make authorize"):
            login = 'tester1'
            password = Generators.get_random_password()
            try:
                Authorize().username_authorize(login=login, password=password)
            except grpc.RpcError as e:
                status_code = e.code()
                assert_that(e)
                assert_that(status_code.value[0], equal_to(3))
                assert_that(status_code.name, equal_to('INVALID_ARGUMENT'))
                assert_that(e.details(), equal_to("Password and login mismatched"))

    @allure.title("Test valid password, invalid login")
    @allure.testcase("XTR-304")
    def test_val_inv(self):
        """
        Failed authorization
        """
        with allure.step("Make authorize"):
            login = Generators.get_random_login()
            password = os.getenv('password')
            try:
                Authorize().username_authorize(login=login, password=password)
            except grpc.RpcError as e:
                status_code = e.code()
                assert_that(e)
                assert_that(status_code.value[0], equal_to(3))
                assert_that(status_code.name, equal_to('INVALID_ARGUMENT'))
                assert_that(e.details(), equal_to("Password and login mismatched"))

    @allure.title("Test invalid password, invalid login")
    @allure.testcase("XTR-303")
    def test_inv_inv(self):
        """
        Failed authorization
        """
        with allure.step("Make authorize"):
            login = Generators.get_random_login()
            password = Generators.get_random_password()
            try:
                res =Authorize().username_authorize(login=login, password=password)
                print(res)
            except grpc.RpcError as e:
                status_code = e.code()
                assert_that(e)
                assert_that(status_code.value[0], equal_to(3))
                assert_that(status_code.name, equal_to('INVALID_ARGUMENT'))
                assert_that(e.details(), equal_to("Password and login mismatched"))