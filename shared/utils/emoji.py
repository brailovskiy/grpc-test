import json
from shared.constants import DefaultValues as DV

def get_emoji_content():
    """ Reading JSON with emoji"""
    # json_db = {'shared/resources/emoji-db.json'}
    with open(DV.json) as f:
        dict_emoji = json.load(f)
        list_emoji = []
    for i in dict_emoji['emojis']:
        list_emoji.append(i[0])
    return list_emoji
