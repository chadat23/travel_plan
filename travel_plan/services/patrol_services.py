from collections import namedtuple
from dataclasses import dataclass
import datetime
from typing import Dict, List, Optional

from sqlalchemy.orm import Session

from travel_plan.models import db_session
from travel_plan.models.patrol_user_units import PatrolUserUnit
from travel_plan.models.patrols import Patrol
from travel_plan.services import location_services, user_services


@dataclass
class PatrolUnit:
    name: str
    pack_color: str
    tent_color: str
    fly_color: str


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
        # patrols = [p[0] for p in patrols]

    except:
        patrols = []
    finally:
        # session.close()
        pass

    return patrols


def add_patrol(start_date: str, entry_point: str, end_date: str, exit_point: str, 
        tracked: bool, plb: str, trip_leader_name: str, 
        patrollers: List[PatrolUnit]
        ):

        session: Session = db_session.create_session()

        if isinstance(start_date, str):
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        if isinstance(end_date, str):
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

        entry_point_id = location_services.get_id_from_name(entry_point)
        exit_point_id = location_services.get_id_from_name(exit_point)
        trip_leader_id = user_services.get_id_from_name(trip_leader_name)

        patrol = Patrol(start_date, entry_point_id, end_date, 
                        exit_point_id, tracked, plb, trip_leader_id)

        session.add(patrol)

        for p in patrollers:

            name = p.name
            pack_color = p.pack_color
            tent_color = p.tent_color
            fly_color = p.fly_color

            if not pack_color:
                pack_color = 'NA'
            if not tent_color:
                tent_color = 'NA'
            if not fly_color:
                fly_color = 'NA'
                
            session.add(PatrolUserUnit(patrol, name, pack_color, tent_color, fly_color))

        session.commit()
        session.close()
