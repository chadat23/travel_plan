import os

import pytest

from sqlalchemy.orm import Session
from travel_plan.models import db_session
from travel_plan.models.cars import Car
from travel_plan.models.colors import Color
from travel_plan.models.locations import Location
from travel_plan.models.travel_days import TravelDay
from travel_plan.models.travel_user_units import TravelUserUnit
from travel_plan.models.users import User
import travel_plan.models.__all_models as all_models

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

_travels = [{'travel': {'start_date': '2019-08-09', 'entry_point': 'May Lake TH',
                        'end_date': '2019-08-11', 'exit_point': 'Ten Lakes TH',
                        'tracked': True, 'plb': 'abc123', 'trip_leader_name': 'Rabbit, Roger',
                        'car_plate': 'G12-123', 'car_make': 'Ford', 'car_model': 'Vroom Queen', 'car_color': 'Red',
                        'car_locaton': 'May Lake TH',
                        'bivy_gear': 'on', 'compass': 'on', 'first_aid_kit': 'on', 'flagging': 'on', 'flare': 'on',
                        'flashlight': 'on',
                        'gps': 'on', 'head_lamp': 'on', 'helmet': 'on', 'ice_axe': 'on', 'map': 'on', 'matches': 'on',
                        'probe_pole': 'on', 'radio': 'on', 'rope': 'on', 'shovel': 'on', 'signal_mirror': 'on',
                        'space_blanket': 'on', 'spare_battery': 'on', 'tent': 'on', 'whistle': 'on',
                        'days_of_food': '3.5', 'weapon': 'None', 'radio_monitor_time': '800-2000',
                        'off_trail_travel': 'no', 'cell_number': '555-132-4567', 'satellite_number': '555-987-6543',
                        'gar_avg': '18.5', 'mitigated_gar': '15', 'gar_mitigations': 'be careful?', 'notes': 'Nope!'
                        },
             'traveler_units': [['Dow, Jane', 'Wild 2', 'Red', 'Green', 'Green', 1, 2, 3, 4, 5, 6, 7, 8, 36],
                                ['Vader, Darth', 'Wild Pi', 'Black', 'Green', 'Red', 9, 8, 7, 6, 5, 4, 3, 2, 44],
                                ['Rabbit, Roger', 'Wild 55', 'Green', 'Green', 'Green', 1, 1, 1, 1, 1, 1, 1, 1, 8],
                                ],
             'day_plans': [{'date': '2019-08-09', 'starting_point': 'May Lake TH', 'ending_point': 'May Lake HSC',
                            'route': 'The trail', 'mode': 'foot'},
                           {'date': '2019-08-10', 'starting_point': 'May Lake HSC', 'ending_point': 'Ten Lakes Basin',
                            'route': 'Still the trail', 'mode': 'foot'},
                           {'date': '2019-08-11', 'starting_point': 'Ten Lakes Basin', 'ending_point': 'May Lake TH',
                            'route': 'More trail', 'mode': 'foot'},
                           ],
             },
            ]


def travels():
    '''
    convert a list of dicts to a list of TravelUserUnits
    and a list of dicts into a list of TravelDays

    This gets around an issue with import order stuff.
    :return:
    '''
    if isinstance(_travels[0]['traveler_units'][0], list):
        for t in _travels:
            t['traveler_units'] = [TravelUserUnit(*u) for u in t['traveler_units']]
            t['day_plans'] = [TravelDay(**d) for d in t['day_plans']]
    return _travels


def clear_db_values():
    classes = dict([(name, cls) for name, cls in all_models.__dict__.items() if isinstance(cls, type)])

    session: Session = db_session.create_session()

    [session.query(cls).delete() for name, cls in classes.items()]

    session.commit()
    session.close()


@pytest.fixture(scope='session')
def db_test_session(tmp_path_factory):
    tmpdir = tmp_path_factory.mktemp("data")

    db = str(tmpdir / 'test.sqlite')

    try:
        db_session.__factory = None
        # session: Session = db_session.global_init('', db)
        session: Session = db_session.global_init(db)
        yield session
    finally:
        os.remove(db)


@pytest.fixture()
def db_session_wo_info(db_test_session: Session):
    yield None

    clear_db_values()


@pytest.fixture()
def db_session_w_info(db_test_session: Session):
    import unittest.mock
    session: Session = db_session.create_session()

    [session.add(Location(**a)) for a in locations]
    [session.add(User(**u)) for u in users]
    [session.add(Color(n)) for n in colors]
    target = 'travel_plan.services.color_services.add_if_not_present'
    test_color = unittest.mock.patch(target, return_value=None)
    with test_color:
        [session.add(Car(**c)) for c in cars]
    session.commit()
    session.close()

    yield locations, users, colors, cars

    clear_db_values()


@pytest.fixture()
def db_users():
    yield users


@pytest.fixture()
def db_locations():
    yield locations


@pytest.fixture()
def db_colors():
    yield colors


@pytest.fixture()
def db_cars():
    yield cars


@pytest.fixture()
def db_session_w_travel_info(db_session_w_info):
    yield travels()
    # yield _travels

# @pytest.fixture()
# def db_session_w_travels(db_session_w_info):
#     import datetime
#
#     from travel_plan.models.travels import Travel
#
#     session: Session = db_session.create_session()
#
#     locations = [n[0] for n in session.query(Location.name).order_by(Location.name).all()]
#
#     for p in travels:
#         user = user_services.get_names()[0]
#         user = user_services.get_user_from_name(user)
#
#         travel = Travel()
#         date = datetime.datetime(p['year'], p['month'], p['start_date'])
#         travel.start_date = date.date()
#         travel.entry_point_id = session.query(Location.id).filter(Location.name == locations[p['start_point']]).first()[
#             0]
#         date = datetime.datetime(p['year'], p['month'], p['end_date'])
#         travel.end_date = date.date()
#         travel.exit_point_id = session.query(Location.id).filter(Location.name == locations[p['exit_point']]).first()[0]
#
#         travel.tracked = p['tracked']
#         travel.plb = p['plb']
#
#         travel.trip_leader_id = session.query(User.id).filter(User.id == p['trip_leader']).first()[0]
#
#         travel_user_unit = TravelUserUnit()
#         travel_user_unit.travel = travel
#         travel_user_unit.traveler = user
#         travel_user_unit.pack_color = 'Green'
#
#         session.add(travel)
#
#         session.add(travel_user_unit)
#
#     session.commit()
#     session.close()
#
#     yield travels
