import json

class Config(object):
    PATH = 'data/credentials.json'

    token = None
    group_id = None

    def load():
        with open(Config.PATH) as cred:
            data = json.loads(cred.read())

        Config.token    = data['token']
        Config.group_id = data['group_id']