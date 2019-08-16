from datetime import datetime
from typing import Optional, List, Dict

from sqlalchemy.orm import Session

from travel_plan.services import location_services
from travel_plan.sql_models import db_session
from travel_plan.sql_models.patrols import Patrol


def get_plans():
    return [
        {'name': 'flask', 'version': '1.2.3'},
        {'name': 'sqlalchemy', 'version': '2.2.0'},
        {'name': 'passlib', 'version': '3.0.0'},
    ]


def create_plan(start_date: str, entry_point: str, end_date: str, exit_point: str, tracked: str, plb: str,
                name0: str, call_sign0: str, pack_color0: str,
                name1: str, call_sign1: str, pack_color1: str,
                name2: str, call_sign2: str, pack_color2: str,
                name3: str, call_sign3: str, pack_color3: str,
                date0: str, start0: str, end0: str, route0: str, mode0: str,
                date1: str, start1: str, end1: str, route1: str, mode1: str,
                date2: str, start2: str, end2: str, route2: str, mode2: str,
                contact0: str, contact1: str,
                ) -> Optional[Patrol]:

    patrol = Patrol()
    patrol.start_date = datetime.strptime(start_date, '%Y-%m-%d')
    patrol.entry_point = entry_point
    patrol.end_date = datetime.strptime(end_date, '%Y-%m-%d')
    patrol.exit_point = exit_point

    patrol.tracked = True if tracked == 'yes' else False
    patrol.plb = plb

    patrol.name0 = name0
    patrol.call_sign0 = call_sign0
    patrol.pack_color0 = pack_color0
    patrol.name1 = name1
    patrol.call_sign1 = call_sign1
    patrol.pack_color1 = pack_color1
    patrol.name2 = name2
    patrol.call_sign2 = call_sign2
    patrol.pack_color2 = pack_color2
    patrol.name3 = name3
    patrol.call_sign3 = call_sign3
    patrol.pack_color3 = pack_color3

    patrol.date0 = None if date0 == '' else datetime.strptime(date0, '%Y-%m-%d')
    patrol.start0 = start0
    patrol.end0 = end0
    patrol.route0 = route0
    patrol.mode0 = mode0
    patrol.date1 = None if date1 == '' else datetime.strptime(date1, '%Y-%m-%d')
    patrol.start1 = start1
    patrol.end1 = end1
    patrol.route1 = route1
    patrol.mode1 = mode1
    patrol.date2 = None if date1 == '' else datetime.strptime(date2, '%Y-%m-%d')
    patrol.start2 = start2
    patrol.end2 = end2
    patrol.route2 = route2
    patrol.mode2 = mode2

    patrol.contact0 = contact0
    patrol.contact1 = contact1

    session: Session = db_session.create_session_patrol()
    try:
        session.add(patrol)
        session.commit()
    finally:
        session.close()

    return patrol


def get_lat_long_frequencies() -> Dict[tuple, int]:
    session: Session = db_session.create_session_patrol()

    patrols: List[Patrol] = list(session.query(Patrol))

    location_name_frequencies = {}

    for patrol in patrols:
        location_name_frequencies = __add_location(patrol.start0, location_name_frequencies)
        location_name_frequencies = __add_location(patrol.start1, location_name_frequencies)
        location_name_frequencies = __add_location(patrol.start2, location_name_frequencies)
        location_name_frequencies = __add_location(patrol.end0, location_name_frequencies)
        location_name_frequencies = __add_location(patrol.end1, location_name_frequencies)
        location_name_frequencies = __add_location(patrol.end2, location_name_frequencies)

    location_coord_frequencies = {}
    loc = {loc.name: loc for loc in location_services.all_locations()}
    for name, freq in location_name_frequencies.items():
        if name in loc:
            location_coord_frequencies[(loc[name].latitude, loc[name].longitude)] = freq

    return location_coord_frequencies


# def __add_point(patrol: Patrol, points) -> Dict[str: List[float, float]]:
def __add_location(point: str, points):
    if point in points:
        points[point] = points[point] + 1
        return points
    points[point] = 1
    return points
