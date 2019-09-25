from typing import List, Optional

from sqlalchemy.orm import Session, joinedload

from travel_plan import db
from travel_plan.models.cars import Car
from travel_plan.services import color_services


def get_names() -> List[str]:

    try:
        cars = db.session.query(Car).options(joinedload(Car.color)).all()
        return [c.name for c in cars]
    except Exception as e:
        print('excepton', e)
        return []


def get_id_from_plate(plate: str):
    try:
        return db.session.query(Car.id).filter(Car.plate == plate).first()[0]
    except:
        return None


def get_plates() -> Optional[List[str]]:
    try:
        return [p[0] for p in db.session.query(Car.plate).filter(Car.active).order_by(Car.plate).all()]
    except:
        return []


def create_car(plate: str, make: str, model: str, color: str, location: str = 'NA', active: bool = True) -> Car:
    '''
    Creates a car object and adds it to the database

    Returns the id of the added car.
    '''
    color = color_services.add_if_not_present(color)

    car = Car(plate, make, model, color, location, active)

    db.session.add(car)
    db.session.commit()

    return car


def get_car(id: int = 0, plate: str = '') -> Car:
    if id:
        a = db.session.query(Car).\
            options(joinedload(Car.color)).\
            filter(Car.id == id).\
            first()
        return a
    elif plate:
        a = db.session.query(Car).\
            options(joinedload(Car.color)).\
            filter(Car.plate == plate).\
            first()
        return a
