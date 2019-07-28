import datetime

import mongoengine


class Patrol(mongoengine.Document):

    start_date = mongoengine.DateField()
    entry_point = mongoengine.StringField()
    end_date = mongoengine.DateField()
    exit_point = mongoengine.StringField()

    tracked = mongoengine.BooleanField()
    plb = mongoengine.StringField()

    name0 = mongoengine.StringField()
    call_sign0 = mongoengine.StringField()
    pack_color0 = mongoengine.StringField()
    name1 = mongoengine.StringField()
    call_sign1 = mongoengine.StringField()
    pack_color1 = mongoengine.StringField()
    name2 = mongoengine.StringField()
    call_sign2 = mongoengine.StringField()
    pack_color2 = mongoengine.StringField()
    name3 = mongoengine.StringField()
    call_sign3 = mongoengine.StringField()
    pack_color3 = mongoengine.StringField()

    date0 = mongoengine.DateField()
    start0 = mongoengine.StringField()
    end0 = mongoengine.StringField()
    route0 = mongoengine.StringField()
    mode0 = mongoengine.StringField()
    date1 = mongoengine.DateField()
    start1 = mongoengine.StringField()
    end1 = mongoengine.StringField()
    route1 = mongoengine.StringField()
    mode1 = mongoengine.StringField()
    date2 = mongoengine.DateField()
    start2 = mongoengine.StringField()
    end2 = mongoengine.StringField()
    route2 = mongoengine.StringField()
    mode2 = mongoengine.StringField()

    contact0 = mongoengine.StringField()
    contact1 = mongoengine.StringField()

    meta = {
        'collection': 'patrol',
        'db_alias': 'core',
        'indexes': [
            'name0',
        ]
    }