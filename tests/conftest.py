import os

import pytest

from sqlalchemy.orm import Session
from travel_plan.models import db_session
from travel_plan.models.cars import Car
from travel_plan.models.colors import Color
from travel_plan.models.locations import Location
from travel_plan.models.patrol_user_units import PatrolUserUnit
from travel_plan.models.users import User
from travel_plan.services import user_services
from travel_plan.services.patrol_services import PatrolUnit

users = [{'name': 'Dow, Jane', 'email': 'chad.derosier+a@gmail.com', 'hashed_ssn': '1',
          'home_phone': '555-123-1234', 'work_phone': '555-123-2345', 'cell_phone': '555-123-3456'},
         {'name': 'Dow, John', 'email': 'chad.derosier+b@gmail.com', 'hashed_ssn': '2',
          'home_phone': '555-234-1234', 'work_phone': '555-234-2345', 'cell_phone': '555-234-3456'},
         {'name': 'Vader, Darth', 'email': 'chad.derosier+c@gmail.com', 'hashed_ssn': '3',
          'home_phone': '555-345-1234', 'work_phone': '555-345-2345', 'cell_phone': '555-345-3456'},
         {'name': 'Rabbit, Roger', 'email': 'chad.derosier+d@gmail.com', 'hashed_ssn': '4',
          'home_phone': '555-456-1234', 'work_phone': '555-456-2345', 'cell_phone': '555-456-3456'},
         {'name': 'Balboa, Rocky', 'email': 'chad.derosier+e@gmail.com', 'hashed_ssn': '5',
          'home_phone': '555-567-1234', 'work_phone': '555-567-2345', 'cell_phone': '555-567-3456'},
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

cars = [{'plate': 'G12-123', 'make': 'Ford', 'model': 'C-Max', 'color': 'White', 'location': 'Yosemite Valley'},
        {'plate': 'G13-587', 'make': 'Ford', 'model': 'F-150', 'color': 'White', 'location': 'Tuolumne'},
        {'plate': 'G13-789', 'make': 'Honda', 'model': 'Element', 'color': 'Blue', 'location': 'El Portal'},
        {'plate': 'G13-875', 'make': 'Nissan', 'model': 'Sentura', 'color': 'Silver', 'location': 'Yosemite Valley'}, ]

colors = ['Red', 'Green', 'Blue', 'Orange', 'Black', 'White']

_patrols = [{'patrol': {'start_date': '2019-08-06', 'entry_point': 'May Lake TH',
                        'end_date': '2019-08-18', 'exit_point': 'Ten Lakes TH',
                        'tracked': True, 'plb': 'abc123', 'trip_leader_name': 'Rabbit, Roger',
                        'car': 'G12-123'},
             'patroller_units': [['Dow, Jane', 'Wild 2', 'Red', 'Green', 'Green', 1, 2, 3, 4, 5, 6, 7, 8],
                                 ['Vader, Darth', 'Wild Pi', 'Black', 'Green', 'Red', 9, 8, 7, 6, 5, 4, 3, 2],
                                 ['Rabbit, Roger', 'Wild 55', 'Green', 'Green', 'Green', 1, 1, 1, 1, 1, 1, 1, 1]
                                 ]
             },
            ]


# @property
def patrols():
    if isinstance(_patrols[0]['patroller_units'][0], list):
        for p in _patrols:
            users = []
            for u in p['patroller_units']:
                users.append(PatrolUserUnit(u[0], u[1], u[2], u[3], u[4], u[5], u[6],
                                            u[7], u[8], u[9], u[10], u[11], u[12]))
            p['patroller_units'] = users

    return _patrols


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
    [session.add(Location(**a)) for a in locations]
    [session.add(User(**u)) for u in users]
    [session.add(Color(id=n)) for n in colors]
    [session.add(Car(**c)) for c in cars]
    session.commit()
    session.close()

    yield locations, users, colors, cars


@pytest.fixture()
def db_session_w_patrol_info(db_session_w_info):
    yield patrols()

# @pytest.fixture()
# def db_session_w_patrols(db_session_w_info):
#     import datetime
#
#     from travel_plan.models.patrols import Patrol
#
#     session: Session = db_session.create_session()
#
#     locations = [n[0] for n in session.query(Location.name).order_by(Location.name).all()]
#
#     for p in patrols:
#         user = user_services.get_names()[0]
#         user = user_services.get_user_from_name(user)
#
#         patrol = Patrol()
#         date = datetime.datetime(p['year'], p['month'], p['start_date'])
#         patrol.start_date = date.date()
#         patrol.entry_point_id = session.query(Location.id).filter(Location.name == locations[p['start_point']]).first()[
#             0]
#         date = datetime.datetime(p['year'], p['month'], p['end_date'])
#         patrol.end_date = date.date()
#         patrol.exit_point_id = session.query(Location.id).filter(Location.name == locations[p['exit_point']]).first()[0]
#
#         patrol.tracked = p['tracked']
#         patrol.plb = p['plb']
#
#         patrol.trip_leader_id = session.query(User.id).filter(User.id == p['trip_leader']).first()[0]
#
#         patrol_user_unit = PatrolUserUnit()
#         patrol_user_unit.patrol = patrol
#         patrol_user_unit.patroller = user
#         patrol_user_unit.pack_color = 'Green'
#
#         session.add(patrol)
#
#         session.add(patrol_user_unit)
#
#     session.commit()
#     session.close()
#
#     yield patrols
