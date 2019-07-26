import datetime

import mongoengine


class Patrol(mongoengine.Document):
    start_date = mongoengine.DateField()
    start_location = mongoengine.IntField()

    end_date = mongoengine.DateField()
    end_location = mongoengine.IntField()

    meta = {
        'collection': 'patrol',
        'db_alias': 'core',
        'indexes': [
            'name',
            'hashed_password',
            'created_date',
        ]
    }