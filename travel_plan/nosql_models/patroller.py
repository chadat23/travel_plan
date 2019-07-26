import datetime

import mongoengine


class Patroller(mongoengine.Document):
    name = mongoengine.StringField()
    call_sign = mongoengine.StringField()
    pack_color = mongoengine.StringField()
    tent_color = mongoengine.StringField()
    fly_color = mongoengine.StringField()
    created_date = mongoengine.DateTimeField(default=datetime.datetime.now)

    meta = {
        'collection': 'patrollers',
        'db_alias': 'core',
        'indexes': [
            'name',
            'call_sign',
        ]
    }

    def __lt__(self, other):
        return self.name < other.name
