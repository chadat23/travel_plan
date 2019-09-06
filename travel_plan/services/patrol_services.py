from collections import namedtuple
from dataclasses import dataclass
import datetime
from typing import Dict, List, Optional

from sqlalchemy.orm import Session

from travel_plan.models import db_session
from travel_plan.models.patrol_user_units import PatrolUserUnit
from travel_plan.models.patrols import Travel
from travel_plan.services import location_services, user_services, car_services


@dataclass
class PatrolUnit:
    name: str
    call_sign: str
    pack_color: str
    tent_color: str
    fly_color: str
    supervision: int
    planning: int
    contingency: int
    comms: int
    team_selection: int
    fitness: int
    env: int
    complexity: int


def get_all(start_date: datetime = '%', entry_point: str = '%', end_date: datetime = '%', exit_point: str = '%',
        limit: int = 20) -> List[str]:
    session: Session = db_session.create_session()

    if entry_point != '%':
        entry_point = location_services.get_id_from_name(entry_point)
    if exit_point != '%':
        exit_point = location_services.get_id_from_name(exit_point)

    try:
        patrols = session.query(Patrol). \
            all()
            # filter(Patrol.start_date.like(start_date)). \
            # filter(Patrol.entry_point.like(entry_point)). \
            # filter(Patrol.end_date.like(end_date)). \
            # filter(Patrol.exit_point.like(exit_point)). \
            # all()

    except:
        patrols = []
    finally:
        session.close()

    return patrols


def add_patrol(start_date: str, entry_point: str, end_date: str, exit_point: str,
               tracked: bool, plb: str, trip_leader_name: str,
               patroller_units: List[PatrolUserUnit], car_name: str, car_location: str
               ):

        session: Session = db_session.create_session()

        if isinstance(start_date, str):
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        if isinstance(end_date, str):
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

        entry_point_id = location_services.get_id_from_name(entry_point)
        exit_point_id = location_services.get_id_from_name(exit_point)
        trip_leader_id = user_services.get_id_from_name(trip_leader_name)

        # If the car name, rather than plate is entered, remove everything after the plate
        car_name: str = car_name.split(' ')[0]
        car_id: int = car_services.get_id_from_plate(car_name)
        car_location: int = location_services.get_id_from_name(car_location)

        patrol = Travel(start_date, entry_point_id, end_date, exit_point_id,
                        tracked, plb, trip_leader_id, car_id, car_location)

        session.add(patrol)

        for p_u in patroller_units:
            if not p_u.pack_color:
                p_u.pack_color = 'NA'
            if not p_u.tent_color:
                p_u.tent_color = 'NA'
            if not p_u.fly_color:
                p_u.fly_color = 'NA'

            p_u.patrol = patrol
                
            session.add(p_u)

        session.commit()
        session.close()

        return patrol
