import requests
import os


def query(user_id):
    return {"query": "{\n  users_item(user_id:" + str(user_id) + "){\n    name\n  }\n}", "variables": {}}


"""
{'data': {'users_item': {'name': 'Zaur Shamilov'}}}
"""


def mutation_create(user_id, title):
    return {
        "query": "mutation {\n  stickers_create_pack(user_id:" + str(user_id) + ", title: \"" + title + "\")\n}\n",
        "variables": {}}


"""
{"data":{"stickers_create_pack":"(2146160365,seq: 0 state: \"\" date: 0)"}}
"""


def mutation_set_share(pack_id):
    return {"query": "mutation {\n  stickers_set_shared(pack_id:" + str(pack_id) + ", is_shared:true)\n}\n",
            "variables": {}}


"""
{"data":{"stickers_set_shared":true}}
"""


def mutation_set_title(pack_id, title):
    return {
        "query": "mutation {\n  stickers_set_title(pack_id:" + str(pack_id) + ", title:\"" + title + "\")\n}\n",
        "variables": {}}


"""
{"data":{"stickers_set_title":"zs_new_titlex"}}
"""


class AdminTools:
    def __init__(self):
        """
        var 'host' sets in main fixture with defining endpoint
        """
        self.auth_url = os.environ["auth_url"]
        self.admin_password = os.getenv('admin_password')
        self.admin_username = os.getenv('admin_username')
        print(self.auth_url)
        self.graph_url = os.environ["graph_url"]
        self.auth_payload = {"username": self.admin_username, "password": self.admin_password}
        self.hed = None
        self.admin_auth()

    def admin_auth(self):
        get_token = requests.post(self.auth_url, json=self.auth_payload)
        data = get_token.json()
        token = data['token']
        self.hed = {'Authorization': 'Bearer ' + token}

    def make_graphql_request(self, query):
        response = requests.post(self.graph_url, json=query, headers=self.hed)
        print(response)
        return response.json()

    def set_url(self):
        return self.auth_url

