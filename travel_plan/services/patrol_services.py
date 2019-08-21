import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from travel_plan.models import db_session
from travel_plan.models.patrols import Patrol
from travel_plan.services import location_services


def get_all(start_date: datetime = '%', entry_point: str = '%', end_date: datetime = '%', exit_point: str = '%',
        limit: int = 10) -> List[str]:
    session: Session = db_session.create_session()

    if entry_point != '%':
        entry_point = location_services.get_id_from_name(entry_point)
    if exit_point != '%':
        exit_point = location_services.get_id_from_name(exit_point)

    try:
        patrols = session.query(Patrol). \
            filter(Patrol.start_date == start_date). \
            filter(Patrol.entry_point == entry_point). \
            filter(Patrol.end_date == end_date). \
            filter(Patrol.exit_point == exit_point). \
            limit(limit).all()
        patrols = [p[0] for p in patrols]

        patrols

    except:
        patrols = []
    finally:
        session.close()

    return patrols
