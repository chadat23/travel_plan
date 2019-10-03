from typing import List, Optional

from travel_plan import db
from travel_plan.location.locations import Location, KindEnum


def get_all() -> List[Location]:
    '''
    Gets all Locations.

    :return: all Locations
    :rtype: List[Location]
    '''
    return db.session.query(Location).all()


def get_names() -> List[str]:
    '''
    Get a complete list of all Location names.

    :return: all location names
    :rtype: List[str]
    '''
    try:
        return [n[0] for n in db.session.query(Location.name).order_by(Location.name).all()]
    except:
        return []


def get_id_from_name(name: str) -> int:
    '''
    Gets the id of a location who's name is supplied.

    :param name: the name of the Location who's id is needed
    :type param: str
    :return: the id of the queried Location
    :rtype: int
    '''
    try:
        return db.session.query(Location.id).filter(Location.name == name).first()[0]
    except:
        return []


def add_location(name: str, latitude: float, longitude: float, kind: KindEnum = KindEnum.Other,
                 note: str = "", is_in_park: bool = True) -> Optional[Location]:
    '''
    Creates a location with the supplied properties and saves it.
    '''

    location = Location(name, latitude, longitude, kind, note, is_in_park)
    db.session.add(location)
    db.session.commit()

    return location


def get_location_from_name(name: str) -> Optional[Location]:
    return db.session.query(Location).filter(Location.name == name).first()
