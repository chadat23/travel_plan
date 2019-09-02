import pytest

_form_data = {'entrydate': '2019-06-18', 'entrypoint': 'May Lake TH',
              'exitdate': '2019-06-20', 'exitpoint': 'May Lake TH',
              'tracked': 'yes', 'plb': '123abc',
              'name0': 'Vader, Darth', 'callsign0': 'Wild 35',
              'packcolor0': 'Red', 'tentcolor0': 'NA', 'flycolor0': 'Blue',
              's0': '1', 'p0': '3', 'cr0': '2', 'c0': '4', 'ts0': '1', 'tf0': '4', 'e0': '1', 'ic0': '3',
              'name1': 'Dow, Jane', 'callsign1': 'Wild 31',
              'packcolor1': 'Green', 'tentcolor1': 'Blue', 'flycolor1': 'Black',
              's1': '2', 'p1': '1', 'cr1': '2', 'c1': '2', 'ts1': '3', 'tf1': '1', 'e1': '2', 'ic1': '2',
              'date0': '2019-06-18', 'start0': 'May Lake TH', 'end0': 'May Lake HSC',
              'route0': 'The trail', 'mode0': 'Foot',
              'date1': '2019-06-19', 'start1': 'May Lake HSC', 'end1': 'Ten Lakes Basin',
              'route1': 'The trail', 'mode1': 'Foot',
              'date2': '2019-06-20', 'start2': 'Ten Lakes Basin', 'end2': 'May Lake TH',
              'route2': 'The trail', 'mode2': 'Foot',
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
              'garavg': '3.84', 'mitigatedavg': '2.5', 'garmitigations': 'Be careful!', 'notes': "Here's a note!",
              }


@pytest.fixture()
def form_data():
    yield _form_data
