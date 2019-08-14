from typing import List

from sqlalchemy.orm import Session

from travel_plan.sql_models import db_session
from travel_plan.sql_models.locations import Location


def all_locations() -> List[Location]:
    session: Session = db_session.create_session_existing()
    try:
        return sorted(list(session.query(Location)))
    finally:
        session.close()


def all_location_names():
    return [i.name for i in all_locations()]
