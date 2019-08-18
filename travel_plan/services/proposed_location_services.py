from sqlalchemy.orm import Session

from travel_plan.models import db_session
from travel_plan.models.proposed_locations import ProposedLocation


def submit_location(name: str, latitude: str, longitude: str, note: str):
    try:
        location = ProposedLocation()
        location.name = name.strip()
        location.latitude = float(latitude.strip())
        location.longitude = float(longitude.strip())
        location.note = note.strip()

        session: Session = db_session.create_session()
        session.add(location)
        session.commit()
        session.close()

        return location
    except:
        return None


def all_locations():
    session: Session = db_session.create_session()
    try:
        return sorted(list(session.query(ProposedLocation)))
    finally:
        session.close()
