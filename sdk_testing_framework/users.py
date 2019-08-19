from shared.data_generators import Generators
from sdk_testing_framework.core import SDK


class Users:
    """
    You don't need to modify this file
    There are some service methods for preparing users for usage in tests
    """

    def __init__(self):
        self.name = Generators.random_dummy_name()

    def get_user(self):
        return SDK(dummy_name=self.name)

    def get_real_user(self, login, password):
        return SDK(login=login, password=password)
