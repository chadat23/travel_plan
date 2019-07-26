import datetime

import mongoengine


class Search(mongoengine.Document):
    item = mongoengine.StringField()
    count = mongoengine.IntField()

    meta = {
        'collection': 'Searches',
        'db_alias': 'core',
        'indexes': [
            'item',
        ]
    }

