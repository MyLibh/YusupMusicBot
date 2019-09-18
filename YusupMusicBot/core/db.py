import os
import json

class db(object):
    PATH = 'data/users.json'

    users = None
    yusup_id = None

    def load():
        if os.path.exists(db.PATH):
            with open(db.PATH, 'r', encoding='utf-8') as file:
                db.users = json.loads(file.read())
        else:
            open(db.PATH, 'x', encoding='utf-8')

    def _save():
        if os.path.exists(db.PATH) == False:
            open(db.PATH, 'x')

        with open(db.PATH, 'w', encoding='utf-8') as file:
            try:
                file.write(unicode(json.dumps(db.users, ensure_ascii=False, indent=4)))
            except NameError:
                file.write(str(json.dumps(db.users, ensure_ascii=False, indent=4)))

    def add_user(id):
        if id not in db.users:
            db.users.append(id)
            db._save()

    def set_yusup_id(api):
        db.yusup_id = api.utils.resolveScreenName(screen_name='big_black_hot_brother')['object_id']

    def remove_user(id):
        if id in db.users:
            db.users.remove(id)
            db._save()