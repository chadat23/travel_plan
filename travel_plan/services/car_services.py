from typing import List, Optional

from sqlalchemy.orm import Session, joinedload

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


def get_car(id: int = 0, plate: str = '') -> Car:
    session: Session = db_session.create_session()

    try:
        if id:
            a = session.query(Car).\
                options(joinedload(Car.color)).\
                filter(Car.id == id).\
                first()
            return a
        elif plate:
            a = session.query(Car).\
                options(joinedload(Car.color)).\
                filter(Car.plate == plate).\
                first()
            return a
    finally:
        session.close()

    return car

