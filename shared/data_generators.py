import os
import random
import string
from shared.utils.emoji import get_emoji_content
from shared.constants import DefaultValues as DV

class Generators:
    def __init__(self):
        pass

    @staticmethod
    def get_random_phone():
        return int('7' + str(random.randint(111_111_1111, 999_999_9999)))

    @staticmethod
    def random_dummy_name(size=8, chars=string.ascii_lowercase):
        return 'at-dummy-' + Generators.random_string(size, chars)

    @staticmethod
    def random_string(size, chars):
        return ''.join(random.choice(chars) for x in range(size))

    @staticmethod
    def random_group_name(size=6, chars=string.ascii_lowercase):
        return 'group-' + Generators.random_string(size, chars)

    @staticmethod
    def random_text_message(size=10, chars=string.ascii_lowercase):
        return 'at-message-' + Generators.random_string(size, chars)

    @staticmethod
    def random_stickerpack(size=10, chars=string.ascii_lowercase):
        return 'at-stickers-' + Generators.random_string(size, chars)

    @staticmethod
    def random_txt_file():
        chars = ''.join([random.choice(string.ascii_letters) for i in range((1024 ** 2)*5)])
        with open(DV.txt, 'w+') as file:
            file.write(chars)
        my_file = DV.txt
        return my_file

    @staticmethod
    def random_emoji():
        list_emoji = get_emoji_content()
        return random.choice(list_emoji)

    @staticmethod
    def get_random_about(size=10, chars=string.ascii_lowercase):
        return 'about ' + Generators.random_string(size, chars)

    @staticmethod
    def get_random_login(size=12, chars=string.ascii_lowercase):
        return Generators.random_string(size, chars)

    @staticmethod
    def get_random_password(size=15, chars=string.ascii_lowercase):
        return Generators.random_string(size, chars)
