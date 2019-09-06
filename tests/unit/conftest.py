import pytest

_form_data = {'entrydate': '2019-06-18', 'entrypoint': 'May Lake TH',
              'exitdate': '2019-06-20', 'exitpoint': 'May Lake TH',
              'tracked': 'yes', 'plb': '123abc',
              'travelername0': 'Vader, Darth', 'callsign0': 'Wild 35',
              'packcolor0': 'Red', 'tentcolor0': 'NA', 'flycolor0': 'Blue',
              'supervision0': '1', 'planning0': '3', 'contingency0': '2', 'comms0': '4', 'teamselection0': '1',
              'fitness0': '4', 'env0': '1', 'complexity0': '3',
              'travelername1': 'Dow, Jane', 'callsign1': 'Wild 31',
              'packcolor1': 'Green', 'tentcolor1': 'Blue', 'flycolor1': 'Black',
              'supervision1': '2', 'planning1': '1', 'contingency1': '2', 'comms1': '2', 'teamselection1': '3',
              'fitness1': '1', 'env1': '2', 'complexity1': '2',
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
              'daysoffood': '3.5', 'weapon': 'None', 'radiomonitortime': '800-2000', 'offtrailtravel': 'yes',
              'cellnumber': '555-132-4567', 'satellitenumber': '555-987-6543',
              'contactemail0': 'email@address.com', 'contactwork0': '555-123-1231',
              'contacthome0': '555-465-4566', 'contactcell0': '555-789-7899',
              'contactemail1': 'email@address.net', 'contactwork1': '555-123-1230',
              'contacthome1': '555-465-4560', 'contactcell1': '555-789-7890',
              'savg': '2', 'pavg': '1', 'cravg': '1', 'cavg': '6', 'tsavg': '1', 'tfavg': '1', 'eavg': '2',
              'icavg': '2',
              'garavg': '3.84', 'mitigatedgar': '2.5', 'garmitigations': 'Be careful!', 'notes': "Here's a note!",
              }


@pytest.fixture()
def form_data():
    yield _form_data.copy()


@pytest.fixture()
def initialized_users(db_users):
    from travel_plan.models.users import User

    users = [User(**u) for u in db_users]

    for i, u in enumerate(users):
        u.id = i + 1

    yield users


@pytest.fixture()
def initialized_locations(db_locations):
    from travel_plan.models.locations import Location

    yield [Location(**a) for a in db_locations]


@pytest.fixture()
def initialized_colors(db_colors):
    from travel_plan.models.colors import Color

    yield [Color(c) for c in db_colors]


@pytest.fixture()
def initialized_cars(db_cars):
    import unittest.mock

    from travel_plan.models.cars import Car

    target = 'travel_plan.services.color_services.add_if_not_present'
    # m = unittest.mock.MagicMock()
    # m.side_effect = 'Red'
    test_color = unittest.mock.patch(target, return_value='Red')
    with test_color:
        cars = [Car(**c) for c in db_cars]

    for i, c in enumerate(cars):
        c.id = i + 1

    yield cars
