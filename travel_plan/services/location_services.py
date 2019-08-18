from typing import List, Optional

from sqlalchemy.orm import Session

from travel_plan.models import db_session
from travel_plan.models.locations import Location


def get_all() -> List[Location]:
    session: Session = db_session.create_session()
    try:
        return session.query(Location).all()
    finally:
        session.close()


# def all_location_names():
#     return [i.name for i in get_all()]


def add_location(name: str, latitude: float, longitude: float) -> Optional[Location]:
    location = Location()
    location.name = name.strip()
    location.latitude = latitude
    location.longitude = longitude

    session: Session = db_session.create_session()
    try:
        session.add(location)
        session.commit()
    finally:
        session.close()

    return location


def get_location(name: str) -> Optional[Location]:
    session: Session = db_session.create_session()
    try:
        location = session.query(Location).filter(Location.name == name).first()
    finally:
        session.close()

    return location
