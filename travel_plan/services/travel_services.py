from datetime import datetime
from typing import List, Dict, Optional

from sqlalchemy.orm import Session, joinedload

from travel_plan.models.travel_user_units import TravelUserUnit
from travel_plan.models.travel_days import TravelDay
from travel_plan.services import car_services, location_services, user_services
from travel_plan.models import db_session
from travel_plan.models.travels import Travel
from travel_plan.models.users import User


def create_plan(start_date: str, entry_point: str, end_date: str, exit_point: str,
                tracked: bool, plb: str, trip_leader_name: str,
                traveler_units: List[TravelUserUnit], day_plans: List[TravelDay],
                car_plate: str, car_make: str, car_model: str, car_color: str, car_location: str,
                bivy_gear: bool,
                compass: bool,
                first_aid_kit: bool,
                flagging: bool,
                flare: bool,
                flashlight: bool,
                gps: bool,
                head_lamp: bool,
                helmet: bool,
                ice_axe: bool,
                map: bool,
                matches: bool,
                probe_pole: bool,
                radio: bool,
                rope: bool,
                shovel: bool,
                signal_mirror: bool,
                space_blanket: bool,
                spare_battery: bool,
                tent: bool,
                whistle: bool,
                days_of_food: str, weapon: str, radio_monitor_time: str,
                off_trail_travel: bool,
                cell_number: str, satellite_number: str,
                contacts: List[User],
                gar_avg: float, mitigated_gar: float, gar_mitigations: str,
                notes: str
                ) -> int:
    car_id = car_services.get_id_from_plate(car_plate.split(' ')[0])
    if not car_id:
        car_id = car_services.create_car(car_plate, car_make, car_model, car_color, car_location, False).id

    entry_point_id = location_services.get_id_from_name(entry_point)
    exit_point_id = location_services.get_id_from_name(exit_point)
    trip_leader_id = user_services.get_id_from_name(trip_leader_name)

    travel = Travel(start_date=datetime.strptime(start_date, '%Y-%m-%d'), entry_point_id=entry_point_id,
                    end_date=datetime.strptime(end_date, '%Y-%m-%d'), exit_point_id=exit_point_id,
                    tracked=tracked, plb=plb, trip_leader_id=trip_leader_id,
                    car_id=car_id, car_location=car_location,
                    bivy_gear=bivy_gear,
                    compass=compass,
                    first_aid_kit=first_aid_kit,
                    flagging=flagging,
                    flare=flare,
                    flashlight=flashlight,
                    gps=gps,
                    head_lamp=head_lamp,
                    helmet=helmet,
                    ice_axe=ice_axe,
                    map=map,
                    matches=matches,
                    probe_pole=probe_pole,
                    radio=radio,
                    rope=rope,
                    shovel=shovel,
                    signal_mirror=signal_mirror,
                    space_blanket=space_blanket,
                    spare_battery=spare_battery,
                    tent=tent,
                    whistle=whistle,
                    days_of_food=days_of_food, weapon=weapon, radio_monitor_time=radio_monitor_time,
                    off_trail_travel=off_trail_travel,
                    cell_number=cell_number, satellite_number=satellite_number,
                    gar_avg=gar_avg, mitigated_gar=mitigated_gar, gar_mitigations=gar_mitigations,
                    notes=notes,
                    )

    contacts = [_verify_contact(c) for c in contacts]
    session: Session = db_session.create_session()
    try:
        session.add(travel)
        for tu in traveler_units:
            tu.travel = travel
            session.add(tu)
        for day in day_plans:
            day.travel = travel
            session.add(day)
        session.commit()
        for contact in contacts:
            contact = session.query(User).filter(User.email == contact.email).first()
            travel.contacts.append(contact)
        session.commit()
    finally:
        session.close()

    return travel.id


def get_travel_by_id(travel_id: int) -> Optional[Travel]:
    session: Session = db_session.create_session()

    try:
        a = session.query(Travel).options(joinedload(Travel.entry_point)).\
            options(joinedload(Travel.car)).\
            options(joinedload(Travel.travelers)).\
            options(joinedload(Travel.travelers).joinedload(TravelUserUnit.traveler)).\
            options(joinedload(Travel.trip_leader)).\
            options(joinedload(Travel.entry_point)).\
            options(joinedload(Travel.exit_point)).\
            options(joinedload(Travel.travel_days).joinedload(TravelDay.starting_point)).\
            options(joinedload(Travel.travel_days).joinedload(TravelDay.ending_point)).\
            options(joinedload(Travel.contacts)).\
            filter(Travel.id == travel_id).first()
        return a
    except:
        return []
    finally:
        session.close()


def _verify_contact(contact: User) -> User:
    existing_contact = user_services.get_user_from_email(contact.email)
    if not existing_contact:
        contact.name = contact.email.split('@')[0].replace('_', '')
        contact.active = False
        return user_services.create_user(user=contact)
    if existing_contact.work_number != contact.work_number or existing_contact.home_number != contact.home_number or \
            existing_contact.cell_number != contact.cell_number:
        return user_services.update_user(existing_contact.id, existing_contact.active, work_number=contact.work_number,
                                         home_number=contact.work_number, cell_number=contact.work_number)
    return existing_contact


def get_lat_long_frequencies() -> Dict[tuple, int]:
    session: Session = db_session.create_session()

    travels: List[Travel] = list(session.query(Travel))

    location_name_frequencies = {}

    for travel in travels:
        location_name_frequencies = __add_location(travel.start0, location_name_frequencies)
        location_name_frequencies = __add_location(travel.start1, location_name_frequencies)
        location_name_frequencies = __add_location(travel.start2, location_name_frequencies)
        location_name_frequencies = __add_location(travel.end0, location_name_frequencies)
        location_name_frequencies = __add_location(travel.end1, location_name_frequencies)
        location_name_frequencies = __add_location(travel.end2, location_name_frequencies)

    location_coord_frequencies = {}
    loc = {loc.name: loc for loc in location_services.get_all()}
    for name, freq in location_name_frequencies.items():
        if name in loc:
            location_coord_frequencies[(loc[name].latitude, loc[name].longitude)] = freq

    return location_coord_frequencies


# def __add_point(travel: Travel, points) -> Dict[str: List[float, float]]:
def __add_location(point: str, points):
    if point in points:
        points[point] = points[point] + 1
        return points
    points[point] = 1
    return points
