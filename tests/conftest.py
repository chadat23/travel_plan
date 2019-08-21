import os

import pytest

from sqlalchemy.orm import Session
from travel_plan.models import db_session
from travel_plan.models.colors import Color
from travel_plan.models.locations import Location
from travel_plan.models.users import User

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

colors = ['Red', 'Green', 'Blue']


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
    [session.add(Color(name=n)) for n in colors]
    session.commit()

    yield locations, users, colors
