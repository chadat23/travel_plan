import os

import pytest

from sqlalchemy.orm import Session
from travel_plan.models import db_session
from travel_plan.models.colors import Color
from travel_plan.models.locations import Location
from travel_plan.models.patrol_user_units import PatrolUserUnit
from travel_plan.models.users import User
from travel_plan.services import user_services
from travel_plan.services.patrol_services import PatrolUnit

users = [{'name': 'Dow, Jane', 'email': 'chad.derosier+a@gmail.com', 'hashed_ssn': '1'},
         {'name': 'Dow, John', 'email': 'chad.derosier+b@gmail.com', 'hashed_ssn': '2'},
         {'name': 'Vader, Darth', 'email': 'chad.derosier+c@gmail.com', 'hashed_ssn': '3'},
         {'name': 'Rabbit, Roger', 'email': 'chad.derosier+d@gmail.com', 'hashed_ssn': '4'},
         {'name': 'Balboa, Rocky', 'email': 'chad.derosier+e@gmail.com', 'hashed_ssn': '5'},
         ]

locations = [{'name': 'Happy Isles TH', 'latitude': 37.732555, 'longitude': -119.557803},
             {'name': 'LYV', 'latitude': 37.733023, 'longitude': -119.514508},
             {'name': 'May Lake HSC', 'latitude': 37.844617, 'longitude': -119.491018},
             {'name': 'May Lake TH', 'latitude': 37.832687, 'longitude': -119.490761},
             {'name': 'Ten Lakes Basin', 'latitude': 37.899158, 'longitude': -119.522609},
             {'name': 'Ten Lakes TH', 'latitude': 37.852321, 'longitude': -119.575861},
             {'name': 'Sunrise Lakes', 'latitude': 37.805904, 'longitude': -119.448250},
             {'name': 'Sunrise Lakes TH', 'latitude': 37.826962, 'longitude': -119.468687},
             ]

colors = ['Red', 'Green', 'Blue', 'Orange', 'Black']

patrols = [{'patrol': {'start_date': '2019-08-16', 'entry_point': 'May Lake TH', 'end_date': '2019-08-18', 'exit_point': 'Ten Lakes TH', 
                       'tracked': True, 'plb': 'abc123', 'trip_leader_name': 'Rabbit, Roger'},
            'users': [PatrolUnit('Dow, Jane', 'Red', 'Green', 'Green'),
                      PatrolUnit('Vader, Darth', 'Black', 'Green', 'Red'),
                      PatrolUnit('Rabbit, Roger', 'Green', 'Green', 'Green')
                      ]
            },
           ]


@pytest.fixture()
def db_test_session(tmpdir):
    db = str(tmpdir / 'test.sqlite')
    try:
        db_session.__factory = None
        session: Session = db_session.global_init('', db)
        yield session
    finally:
        os.remove(db)


@pytest.fixture()
def db_session_w_info(db_test_session: Session):
    session: Session = db_session.create_session()
    [session.add(Location(name=a['name'], latitude=a['latitude'], longitude=a['longitude'])) for a in locations]
    [session.add(User(name=u['name'], email=u['email'], hashed_ssn=u['hashed_ssn'])) for u in users]
    [session.add(Color(id=n)) for n in colors]
    session.commit()
    session.close()

    yield locations, users, colors


@pytest.fixture()
def db_session_w_patrol_info(db_session_w_info):
    yield patrols


@pytest.fixture()
def db_session_w_patrols(db_session_w_info):
    import datetime

    from travel_plan.models.patrols import Patrol

    session: Session = db_session.create_session()

    locations = [n[0] for n in session.query(Location.name).order_by(Location.name).all()]

    for p in patrols:
        user = user_services.get_names()[0]
        user = user_services.get_user_from_name(user)

        patrol = Patrol()
        date = datetime.datetime(p['year'], p['month'], p['start_date'])
        patrol.start_date = date.date()
        patrol.entry_point_id = session.query(Location.id).filter(Location.name == locations[p['start_point']]).first()[0]
        date = datetime.datetime(p['year'], p['month'], p['end_date'])
        patrol.end_date = date.date()
        patrol.exit_point_id = session.query(Location.id).filter(Location.name == locations[p['exit_point']]).first()[0]

        patrol.tracked = p['tracked']
        patrol.plb = p['plb']

        patrol.trip_leader_id = session.query(User.id).filter(User.id == p['trip_leader']).first()[0]

        patrol_user_unit = PatrolUserUnit()
        patrol_user_unit.patrol = patrol
        patrol_user_unit.patroller = user
        patrol_user_unit.pack_color = 'Green'

        session.add(patrol)

        session.add(patrol_user_unit)



    session.commit()
    session.close()

    yield patrols
