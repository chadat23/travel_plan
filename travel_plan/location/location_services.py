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


def get_id_by_name(name: str) -> int:
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


def add_location(name: str, latitude: float = None, longitude: float = None, kind: KindEnum = None,
                 note: str = None, is_in_park: bool = None) -> Optional[Location]:
    '''
    Creates a location with the supplied properties and saves it.

    :param name: the name of the location
    :type name: str
    :param latitude: the latitude of the location
    :type name: float
    :param longitude: the longitude of the location
    :type name: float
    :param kind: what the location is: lake, river, peak, 
    trailhead, campground, etc.
    :type kind: KindEnum
    :param note: Any notes deemed relevant for the location.
    :type note: str
    :param is_in_park: whether or not the location is in the park
    True for yes, False for no
    :type is_in_park: bool
    :return: the location if it was created, None if for whatever
    reason it wasn't
    :rtype: Optional[Location]
    '''

    try:
        location = Location(name, latitude, longitude, kind, note, is_in_park)
        db.session.add(location)
        db.session.commit()
        return location
    except:
        return None


def get_location_by_name(name: str) -> Optional[Location]:
    '''
    Gets the Location who's name matches the supplied name.

    :param name: the name of the Location that's to be retrieved
    :type name: str
    :return: the location with the matching name
    :rtype: Location if one's found, otherwise None
    '''
    return db.session.query(Location).filter(Location.name == name).first()
