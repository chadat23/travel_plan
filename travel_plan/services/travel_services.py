from datetime import datetime
from typing import Optional, List, Dict

from sqlalchemy.orm import Session

from travel_plan.models.patrol_user_units import PatrolUserUnit
from travel_plan.models.patrol_days import PatrolDay
from travel_plan.services import car_services, location_services
from travel_plan.models import db_session
from travel_plan.models.patrols import Patrol


def create_plan(start_date: str, entry_point: str, end_date: str, exit_point: str, tracked: str, plb: str,
                patroller_units: List[PatrolUserUnit], day_plans: List[PatrolDay],
                car_plate: str, car_make: str, car_model: str, car_color: str, car_location: str,
                bivy_gear: bool, compass: bool, first_aid_kit: bool, flagging: bool, flare: bool, flashlight: bool,
                gps: bool, head_lamp: bool, helmet: bool, ice_axe: bool, map: bool, matches: bool, probe_pole: bool,
                radio: bool, rope: bool, shovel: bool, signal_mirror: bool, space_blanket: bool, spare_battery: bool,
                tent: bool, whistle: bool,
                contact0: str, contact1: str,
                ) -> Optional[Patrol]:

    patrol = Patrol()
    patrol.start_date = datetime.strptime(start_date, '%Y-%m-%d')
    patrol.entry_point = entry_point
    patrol.end_date = datetime.strptime(end_date, '%Y-%m-%d')
    patrol.exit_point = exit_point

    patrol.tracked = True if tracked == 'yes' else False
    patrol.plb = plb

    car_id = car_services.get_id_from_plate(car_plate.split(' ')[0])
    if not car_id:
        car_id = car_services.create_car(car_plate, car_make, car_model, car_color, car_location, False)

    self.bivy_gear = bivy_gear
    self.compass = compass
    self.first_aid_kit = first_aid_kit
    self.flagging = flagging
    self.flare = flare
    self.flashlight = flashlight
    self.gps = gps
    self.head_lamp = head_lamp
    self.helmet = helmet
    self.ice_axe = ice_axe
    self.map = map
    self.matches = matches
    self.probe_pole = probe_pole
    self.radio = radio
    self.rope = rope
    self.shovel = shovel
    self.signal_mirror = signal_mirror
    self.space_blanket = space_blanket
    self.spare_battery = spare_battery
    self.tent = tent
    self.whistle = whistle

    patrol.contact0 = contact0
    patrol.contact1 = contact1

    session: Session = db_session.create_session()
    try:
        session.add(patrol)
        session.commit()
    finally:
        session.close()

    return patrol


def get_lat_long_frequencies() -> Dict[tuple, int]:
    session: Session = db_session.create_session()

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
    loc = {loc.name: loc for loc in location_services.get_all()}
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
