from typing import List, Optional

from sqlalchemy.orm import Session

from travel_plan.models import db_session
from travel_plan.models.cars import Car
from travel_plan.services import color_services


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
        return [p[0] for p in session.query(Car.plate).filter(Car.active).order_by(Car.plate).all()]
    except:
        return []
    finally:
        session.close()


def create_car(plate: str, make: str, model: str, color: str, location: str = 'NA', active: bool = True) -> Car:
    '''
    Creates a car object and adds it to the database

    Returns the id of the added car.    
    '''
    session: Session = db_session.create_session()

    color = color_services.add_if_not_present(color)

    car = Car(plate, make, model, color, location, active)
    try:
        session.add(car)
        session.commit()
    finally:
        session.close()

    return car
