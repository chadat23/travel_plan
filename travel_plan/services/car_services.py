from typing import List, Optional

from sqlalchemy.orm import Session

from travel_plan.models import db_session
from travel_plan.models.cars import Car


def get_names() -> List[str]:
    session: Session = db_session.create_session()

    try:
        cars: List[Car] = session.query(Car).order_by(Car.location, Car.plate).all()
        return [c.name for c in cars]
    except:
        return []
    finally:
        session.close()


def get_id_from_plate(plate: str):
    session: Session = db_session.create_session()

    try:
        return session.query(Car.id).filter(Car.plate == plate).first()[0]
    except:
        return None
    finally:
        session.close()


def get_plates() -> Optional[List[str]]:
    session: Session = db_session.create_session()

    try:
        return [p[0] for p in session.query(Car.plate).order_by(Car.plate).all()]
    except:
        return []
    finally:
        session.close()
