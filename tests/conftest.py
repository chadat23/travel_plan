import os

import pytest

from sqlalchemy.orm import Session
from travel_plan.models import db_session
from travel_plan.models.locations import Location
from travel_plan.models.users import User

users = [{'name': 'Jane Dow', 'email': 'chad.derosier+a@gmail.com', 'hashed_ssn': '1'},
         {'name': 'John Dow', 'email': 'chad.derosier+b@gmail.com', 'hashed_ssn': '2'},
         {'name': 'Darth Vader', 'email': 'chad.derosier+c@gmail.com', 'hashed_ssn': '3'},
         {'name': 'Roger Rabbit', 'email': 'chad.derosier+d@gmail.com', 'hashed_ssn': '4'},
         {'name': 'Rocky Balboa', 'email': 'chad.derosier+e@gmail.com', 'hashed_ssn': '5'},
         ]

locations = [{'name': 'Happy Isles TH', 'lat': 37.732555, 'long': -119.557803},
             {'name': 'LYV', 'lat': 37.733023, 'long': -119.514508},
             {'name': 'May Lake HSC', 'lat': 37.844617, 'long': -119.491018},
             {'name': 'May Lake TH', 'lat': 37.832687, 'long': -119.490761},
             {'name': 'Ten Lakes Basin', 'lat': 37.899158, 'long': -119.522609},
             {'name': 'Ten Lakes TH', 'lat': 37.852321, 'long': -119.575861},
             {'name': 'Sunrise Lakes', 'lat': 37.805904, 'long': -119.448250},
             {'name': 'Sunrise Lakes TH', 'lat': 37.826962, 'long': -119.468687},
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
    [session.add(Location(name=a['name'], latitude=a['lat'], longitude=a['long'])) for a in locations]
    [session.add(User(name=u['name'], email=u['email'], hashed_ssn=u['hashed_ssn'])) for u in users]
    session.commit()

    yield session
