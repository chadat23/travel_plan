import copy
import os

import pytest

from travel_plan import create_app
from travel_plan.location.locations import KindEnum

_form_data = {'startdate': '2019-06-18', 'entrypoint': 'May Lake TH',
              'enddate': '2019-06-20', 'exitpoint': 'May Lake TH',
              'tracked': 'yes', 'plb': '123abc',
              'travelername0': 'Vader, Darth', 'callsign0': 'Wild 35',
              'packcolor0': 'Red', 'tentcolor0': 'NA', 'flycolor0': 'Blue',
              'supervision0': '1', 'planning0': '3', 'contingency0': '2', 'comms0': '4', 'teamselection0': '1',
              'fitness0': '4', 'env0': '1', 'complexity0': '3', 'total0': '19',
              'travelername1': 'Doe, Jane', 'callsign1': 'Wild 31',
              'packcolor1': 'Green', 'tentcolor1': 'Blue', 'flycolor1': 'Black',
              'supervision1': '2', 'planning1': '1', 'contingency1': '2', 'comms1': '2', 'teamselection1': '3',
              'fitness1': '1', 'env1': '2', 'complexity1': '2', 'total1': '15',
              'date0': '2019-06-18', 'startingpoint0': 'May Lake TH', 'endingpoint0': 'May Lake HSC',
              'route0': 'The trail', 'mode0': 'Foot',
              'date1': '2019-06-19', 'startingpoint1': 'May Lake HSC', 'endingpoint1': 'Ten Lakes Basin',
              'route1': 'Still the trail', 'mode1': 'Foot',
              'date2': '2019-06-20', 'startingpoint2': 'Ten Lakes Basin', 'endingpoint2': 'May Lake TH',
              'route2': 'More of the trail', 'mode2': 'Foot',
              'carplate': 'G12-123', 'carmake': 'Ford', 'carmodel': 'C-Max', 'carcolor': 'White',
              'carlocation': 'May Lake TH',
              'bivygear': 'on', 'compass': 'on', 'firstaidkit': 'on', 'flagging': 'on', 'flare': 'on',
              'flashlight': 'on',
              'gps': 'on', 'headlamp': 'on', 'helmet': 'on', 'iceaxe': 'on', 'map': 'on', 'matches': 'on',
              'probepole': 'on', 'radio': 'on', 'rope': 'on', 'shovel': 'on', 'signalmirror': 'on',
              'spaceblanket': 'on',
              'sparebattery': 'on', 'tent': 'on', 'whistle': 'on',
              'daysoffood': '3.5', 'weapon': 'None', 'radiomonitortime': '800-2000', 'offtrailtravel': 'no',
              'cellnumber': '555-132-4567', 'satellitenumber': '555-987-6543',
              'contactname0': 'McCallister, Kevin', 'contactemail0': 'ilovecats@address.com',
              'contactwork0': '555-123-1231', 'contacthome0': '555-465-4566', 'contactcell0': '555-789-7899',
              'contactname1': 'Powell, Harry', 'contactemail1': 'ilovedogs@address.net',
              'contactwork1': '555-123-1230', 'contacthome1': '555-465-4560', 'contactcell1': '555-789-7890',
              'garavg': '3.84', 'mitigatedgar': '2.5', 'garmitigations': 'Be careful!\nTake chances!',
              'notes': "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Erat nam at lectus urna duis convallis convallis. Eget mi proin sed libero enim. Sem integer vitae justo eget. Et netus et malesuada fames ac turpis egestas maecenas. Arcu vitae elementum curabitur vitae nunc sed. Cursus mattis molestie a iaculis at erat pellentesque adipiscing. Ipsum dolor sit amet consectetur adipiscing elit ut aliquam. Id porta nibh venenatis cras sed. At varius vel pharetra vel turpis nunc. Id donec ultrices tincidunt arcu non. Nullam non nisi est sit amet. Elementum curabitur vitae nunc sed. Sodales ut etiam sit amet nisl purus in mollis nunc.",
              }

_form_data_w_nones = {'startdate': '2019-06-18', 'entrypoint': 'May Lake TH',
                      'enddate': '2019-06-20', 'exitpoint': 'May Lake TH',
                      'tracked': 'yes', 'plb': '',
                      'travelername0': 'Vader, Darth', 'callsign0': '', 'packcolor0': '', 'tentcolor0': '',
                      'flycolor0': '',
                      'supervision0': '1', 'planning0': '3', 'contingency0': '2', 'comms0': '4', 'teamselection0': '1',
                      'fitness0': '4', 'env0': '1', 'complexity0': '3', 'total0': '19',
                      'date0': '2019-06-18', 'startingpoint0': 'May Lake TH', 'endingpoint0': 'May Lake HSC',
                      'route0': 'The trail', 'mode0': 'Foot',
                      'date1': '2019-06-19', 'startingpoint1': 'May Lake HSC', 'endingpoint1': 'Ten Lakes Basin',
                      'route1': 'Still the trail', 'mode1': 'Foot',
                      'date2': '2019-06-20', 'startingpoint2': 'Ten Lakes Basin', 'endingpoint2': 'May Lake TH',
                      'route2': 'More of the trail', 'mode2': 'Foot',
                      'carplate': '', 'carmake': '', 'carmodel': '', 'carcolor': '', 'carlocation': 'May Lake TH',
                      'bivygear': 'on', 'compass': 'on', 'firstaidkit': 'on', 'flagging': 'on', 'flare': 'on',
                      'flashlight': 'on',
                      'gps': 'on', 'headlamp': 'on', 'helmet': 'on', 'iceaxe': 'on', 'map': 'on', 'matches': 'on',
                      'probepole': 'on', 'radio': 'on', 'rope': 'on', 'shovel': 'on', 'signalmirror': 'on',
                      'spaceblanket': 'on',
                      'sparebattery': 'on', 'tent': 'on', 'whistle': 'on',
                      'daysoffood': '3.5', 'weapon': '', 'radiomonitortime': '', 'offtrailtravel': 'no',
                      'cellnumber': '', 'satellitenumber': '',
                      'contactname0': 'Doe, Jane', 'contactemail0': '',
                      'contactwork0': '', 'contacthome0': '', 'contactcell0': '',
                      'contactname1': '', 'contactemail1': '',
                      'contactwork1': '', 'contacthome1': '', 'contactcell1': '',
                      'garavg': '3.84', 'mitigatedgar': '2.5', 'garmitigations': '',
                      'notes': '',
                      }

_departments = [{'name': 'Wilderness'}]

_users = [{'name': 'Doe, Jane', 'email': 'chad.derosier+a@gmail.com', 'home_number': '555-123-1234',
           'work_number': '555-123-2345', 'cell_number': '555-123-3456', 'department': 'Wilderness', 'active': True},
          {'name': 'Doe, John', 'email': 'chad.derosier+b@gmail.com', 'home_number': '555-234-1234',
           'work_number': '555-234-2345', 'cell_number': '555-234-3456', 'department': 'Wilderness', 'active': True},
          {'name': 'Vader, Darth', 'email': 'chad.derosier+c@gmail.com', 'home_number': '555-345-1234',
           'work_number': '555-345-2345', 'cell_number': '555-345-3456', 'department': 'Wilderness', 'active': True},
          {'name': 'Rabbit, Roger', 'email': 'chad.derosier+d@gmail.com', 'home_number': '555-456-1234',
           'work_number': '555-456-2345', 'cell_number': '555-456-3456', 'department': 'Wilderness', 'active': True},
          {'name': 'Balboa, Rocky', 'email': 'chad.derosier+e@gmail.com', 'home_number': '555-567-1234',
           'work_number': '555-567-2345', 'cell_number': '555-567-3456', 'department': 'Wilderness', 'active': True},
          ]

_locations = [
    {'name': 'Happy Isles TH', 'latitude': 37.732555, 'longitude': -119.557803, 'kind': KindEnum.Trail_Head, 'note': '',
     'is_in_park': True},
    {'name': 'LYV', 'latitude': 37.733023, 'longitude': -119.514508, 'kind': KindEnum.Campground, 'note': '',
     'is_in_park': True},
    {'name': 'May Lake HSC', 'latitude': 37.844617, 'longitude': -119.491018, 'kind': KindEnum.Campground, 'note': '',
     'is_in_park': True},
    {'name': 'May Lake TH', 'latitude': 37.832687, 'longitude': -119.490761, 'kind': KindEnum.Trail_Head, 'note': '',
     'is_in_park': True},
    {'name': 'Ten Lakes Basin', 'latitude': 37.899158, 'longitude': -119.522609, 'kind': KindEnum.Basin, 'note': '',
     'is_in_park': True},
    {'name': 'Ten Lakes TH', 'latitude': 37.852321, 'longitude': -119.575861, 'kind': KindEnum.Trail_Head, 'note': '',
     'is_in_park': True},
    {'name': 'Sunrise Lakes', 'latitude': 37.805904, 'longitude': -119.448250, 'kind': KindEnum.Area, 'note': '',
     'is_in_park': True},
    {'name': 'Sunrise Lakes TH', 'latitude': 37.826962, 'longitude': -119.468687, 'kind': KindEnum.Trail_Head,
     'note': '', 'is_in_park': True},
]

_cars = [{'plate': 'G12-123', 'make': 'Ford', 'model': 'C-Max', 'color': 'White', 'location': 'Yosemite Valley',
          'active': True, 'department': 'Wilderness'},
         {'plate': 'G13-587', 'make': 'Ford', 'model': 'F-150', 'color': 'White', 'location': 'Tuolumne',
          'active': True, 'department': 'Wilderness'},
         {'plate': 'G13-789', 'make': 'Honda', 'model': 'Element', 'color': 'Blue', 'location': 'El Portal',
          'active': True, 'department': 'Wilderness'},
         {'plate': 'G13-875', 'make': 'Nissan', 'model': 'Sentura', 'color': 'Silver', 'location': 'Yosemite Valley',
          'active': True, 'department': 'Wilderness'},
         ]

_colors = ['Red', 'Green', 'Blue', 'Orange', 'Black', 'White']

_travels = [{'travel': {'start_date': '2019-08-09', 'entry_point': 'May Lake TH',
                        'end_date': '2019-08-11', 'exit_point': 'Ten Lakes TH',
                        'tracked': True, 'plb': 'abc123', 'trip_leader_name': 'Rabbit, Roger',
                        'car_plate': 'G12-123', 'car_make': 'Ford', 'car_model': 'Vroom Queen', 'car_color': 'Red',
                        'car_location': 'May Lake TH',
                        'bivy_gear': 'on', 'compass': 'on', 'first_aid_kit': 'on', 'flagging': 'on', 'flare': 'on',
                        'flashlight': 'on',
                        'gps': 'on', 'head_lamp': 'on', 'helmet': 'on', 'ice_axe': 'on', 'map': 'on', 'matches': 'on',
                        'probe_pole': 'on', 'radio': 'on', 'rope': 'on', 'shovel': 'on', 'signal_mirror': 'on',
                        'space_blanket': 'on', 'spare_battery': 'on', 'tent': 'on', 'whistle': 'on',
                        'days_of_food': '3.5', 'weapon': 'None', 'radio_monitor_time': '800-2000',
                        'off_trail_travel': False, 'cell_number': '555-132-4567', 'satellite_number': '555-987-6543',
                        'gar_avg': '18.5', 'mitigated_gar': '15',
                        'gar_mitigations': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Erat nam at lectus urna duis convallis convallis. Eget mi proin sed libero enim. Sem integer vitae justo eget. Et netus et malesuada fames ac turpis egestas maecenas. Arcu vitae elementum curabitur vitae nunc sed. Cursus mattis molestie a iaculis at erat pellentesque adipiscing. Ipsum dolor sit amet consectetur adipiscing elit ut aliquam. Id porta nibh venenatis cras sed. At varius vel pharetra vel turpis nunc. Id donec ultrices tincidunt arcu non. Nullam non nisi est sit amet. Elementum curabitur vitae nunc sed. Sodales ut etiam sit amet nisl purus in mollis nunc.',
                        'notes': 'Nope!',
                        'files': ['travel_file.pdf', 'travel_file_1.jpg']
                        },
             'traveler_units': [['Doe, Jane', 'Wild 2', 'Red', 'Green', 'Green', 1, 2, 3, 4, 5, 6, 7, 8, 36],
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
             'contacts': [{'name': 'Coworker 1', 'email': 'chad.derosier+f@gmail.com', 'work_number': '555-1234',
                           'home_number': '555-2345', 'cell_number': '555-3456'},
                          {'name': 'Coworker 2', 'email': 'chad.derosier+g@gmail.com', 'work_number': '555-2234',
                           'home_number': '555-3345', 'cell_number': '555-4456'}
                          ],
             'files': [{'name': 'Doe_Jane_20190809.pdf'}, {'name': 'Doe_Jane_20190809_1.jpg'}]
             },
            ]

_travels_w_nones = [{'travel': {'start_date': '2019-08-09', 'entry_point': 'May Lake TH',
                                'end_date': '2019-08-11', 'exit_point': 'Ten Lakes TH',
                                'tracked': True, 'plb': None, 'trip_leader_name': 'Rabbit, Roger',
                                'car_plate': None, 'car_make': None, 'car_model': None, 'car_color': None,
                                'car_location': None,
                                'bivy_gear': 'on', 'compass': 'on', 'first_aid_kit': 'on', 'flagging': 'on',
                                'flare': 'on',
                                'flashlight': 'on',
                                'gps': 'on', 'head_lamp': 'on', 'helmet': 'on', 'ice_axe': 'on', 'map': 'on',
                                'matches': 'on',
                                'probe_pole': 'on', 'radio': 'on', 'rope': 'on', 'shovel': 'on', 'signal_mirror': 'on',
                                'space_blanket': 'on', 'spare_battery': 'on', 'tent': 'on', 'whistle': 'on',
                                'days_of_food': '3.5', 'weapon': None, 'radio_monitor_time': None,
                                'off_trail_travel': False, 'cell_number': None, 'satellite_number': None,
                                'gar_avg': '18.5', 'mitigated_gar': '15', 'gar_mitigations': None, 'notes': None,
                                'files': None
                                },
                     'traveler_units': [['Doe, Jane', None, None, None, None, 1, 2, 3, 4, 5, 6, 7, 8, 36],
                                        ],
                     'day_plans': [
                         {'date': '2019-08-09', 'starting_point': 'May Lake TH', 'ending_point': 'May Lake HSC',
                          'route': 'The trail', 'mode': 'foot'},
                         {'date': '2019-08-10', 'starting_point': 'May Lake HSC', 'ending_point': 'Ten Lakes Basin',
                          'route': 'Still the trail', 'mode': 'foot'},
                         {'date': '2019-08-11', 'starting_point': 'Ten Lakes Basin', 'ending_point': 'May Lake TH',
                          'route': 'More trail', 'mode': 'foot'},
                         ],
                     'contacts': [{'name': 'Doe, Jane', 'email': None, 'work_number': None,
                                   'home_number': None, 'cell_number': None},
                                  ],
                     'files': []
                     },
                    ]


@pytest.fixture(scope='session')
def app(tmp_path_factory):
    from travel_plan.config import Config

    config = copy.deepcopy(Config)

    tmpdir = tmp_path_factory.mktemp("test")

    config.DB_FOLDER_PATH = str(tmpdir)
    config.PDF_FOLDER_PATH = str(tmpdir)

    db_path = str(tmpdir / 'test.sqlite')
    config.SQLALCHEMY_DATABASE_URI = 'sqlite:///' + db_path

    config.DEFAULT_EMAIL_LIST = []

    app = create_app(config)
    app.config['TESTING'] = True

    yield app

    os.remove(db_path)


@pytest.fixture()
def app_w_empty_db(app):
    from travel_plan import db

    # with app.app_context():
    db.create_all()

    yield app

    # with app.app_context():
    db.session.close()
    db.drop_all()


@pytest.fixture()
def app_w_db(app_w_empty_db):
    # with app_w_empty_db.app_context():
    from travel_plan import db
    from travel_plan.car.cars import Car
    from travel_plan.color.colors import Color
    from travel_plan.department.departments import Department
    from travel_plan.location.locations import Location
    from travel_plan.user.users import User

    [db.session.add(Department(**d)) for d in _departments]
    [db.session.add(Color(c)) for c in _colors]
    [db.session.add(Car(**c)) for c in _cars]
    [db.session.add(Location(**loc)) for loc in _locations]
    [db.session.add(User(**u)) for u in _users]

    db.session.commit()

    yield app_w_empty_db


@pytest.fixture()
def form_data():
    yield _form_data.copy()


@pytest.fixture()
def form_data_w_nones():
    yield _form_data_w_nones.copy()


@pytest.fixture()
def cars():
    yield _cars


@pytest.fixture()
def colors():
    yield _colors


@pytest.fixture()
def departments():
    yield _departments


@pytest.fixture()
def locations():
    yield _locations


@pytest.fixture()
def travels(app_w_db):
    yield _make_travels(_travels)


@pytest.fixture()
def travels_w_nones(app_w_db):
    yield _make_travels(_travels_w_nones)


@pytest.fixture()
def users():
    yield _users


@pytest.fixture()
def travel_object(app_w_db):
    from travel_plan.travel.travel_services import create_plan, get_travel_by_id

    _travel = _make_travels(_travels)[0]
    t = _travel['travel']
    traveler_units = _travel['traveler_units']
    day_plans = _travel['day_plans']
    contacts = _travel['contacts']
    files = _travel['files']

    id = create_plan(t['start_date'], t['entry_point'], t['end_date'], t['exit_point'],
                     t['tracked'], t['plb'], t['trip_leader_name'], traveler_units, day_plans,
                     t['car_plate'], t['car_make'], t['car_model'], t['car_color'], t['car_location'],
                     t['bivy_gear'] == 'on', t['compass'] == 'on', t['first_aid_kit'] == 'on', t['flagging'] == 'on',
                     t['flare'] == 'on',
                     t['flashlight'] == 'on', t['gps'] == 'on', t['head_lamp'] == 'on', t['helmet'] == 'on',
                     t['ice_axe'] == 'on', t['map'] == 'on',
                     t['matches'] == 'on', t['probe_pole'] == 'on', t['radio'] == 'on', t['rope'] == 'on',
                     t['shovel'] == 'on', t['signal_mirror'] == 'on',
                     t['space_blanket'] == 'on', t['spare_battery'] == 'on', t['tent'] == 'on', t['whistle'] == 'on',
                     t['days_of_food'], t['weapon'], t['radio_monitor_time'], t['off_trail_travel'],
                     t['cell_number'], t['satellite_number'], contacts,
                     t['gar_avg'], t['mitigated_gar'], t['gar_mitigations'], t['notes'], files)

    travel = get_travel_by_id(id)

    yield travel


@pytest.fixture()
def travel_object_w_nones(app_w_db):
    from travel_plan.travel.travel_services import create_plan, get_travel_by_id

    _travel = _make_travels(_travels_w_nones)[0]
    t = _travel['travel']
    traveler_units = _travel['traveler_units']
    day_plans = _travel['day_plans']
    contacts = _travel['contacts']
    files = _travel['files']

    id = create_plan(t['start_date'], t['entry_point'], t['end_date'], t['exit_point'],
                     t['tracked'], t['plb'], t['trip_leader_name'], traveler_units, day_plans,
                     t['car_plate'], t['car_make'], t['car_model'], t['car_color'], t['car_location'],
                     t['bivy_gear'] == 'on', t['compass'] == 'on', t['first_aid_kit'] == 'on', t['flagging'] == 'on',
                     t['flare'] == 'on',
                     t['flashlight'] == 'on', t['gps'] == 'on', t['head_lamp'] == 'on', t['helmet'] == 'on',
                     t['ice_axe'] == 'on', t['map'] == 'on',
                     t['matches'] == 'on', t['probe_pole'] == 'on', t['radio'] == 'on', t['rope'] == 'on',
                     t['shovel'] == 'on', t['signal_mirror'] == 'on',
                     t['space_blanket'] == 'on', t['spare_battery'] == 'on', t['tent'] == 'on', t['whistle'] == 'on',
                     t['days_of_food'], t['weapon'], t['radio_monitor_time'], t['off_trail_travel'],
                     t['cell_number'], t['satellite_number'], contacts,
                     t['gar_avg'], t['mitigated_gar'], t['gar_mitigations'], t['notes'], files)

    travel = get_travel_by_id(id)

    yield travel


def _make_travels(_travels):
    """
    convert a list of dicts to a list of TravelUserUnits
    and a list of dicts into a list of TravelDays

    This gets around an issue with import order stuff.
    :return:
    """

    from travel_plan.travel.travel_user_units import TravelUserUnit
    from travel_plan.travel.travel_days import TravelDay
    from travel_plan.user.users import User
    from travel_plan.travel.travel_file import TravelFile

    travel = copy.deepcopy(_travels)
    for t in travel:
        t['traveler_units'] = [TravelUserUnit(*u) for u in t['traveler_units']]
        t['day_plans'] = [TravelDay(**d) for d in t['day_plans']]
        t['contacts'] = [User(**u) for u in t['contacts']]
        t['files'] = [TravelFile(**f) for f in t['files']]
    return travel


@pytest.fixture()
def initialized_users(users):
    from travel_plan.user.users import User

    users = [User(**u) for u in users]

    for i, u in enumerate(users):
        u.id = i + 1

    yield users


@pytest.fixture()
def initialized_locations(locations):
    from travel_plan.location.locations import Location

    yield [Location(**a) for a in locations]


@pytest.fixture()
def initialized_colors(colors):
    from travel_plan.color.colors import Color

    yield [Color(c) for c in colors]


@pytest.fixture()
def initialized_cars(cars):
    import unittest.mock

    from travel_plan.car.cars import Car

    target = 'travel_plan.services.color_services.add_if_not_present'
    # m = unittest.mock.MagicMock()
    # m.side_effect = 'Red'
    test_color = unittest.mock.patch(target, return_value='Red')
    with test_color:
        cars = [Car(**c) for c in cars]

    for i, c in enumerate(cars):
        c.id = i + 1

    yield cars
