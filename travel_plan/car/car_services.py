from typing import List, Optional

from sqlalchemy.orm import joinedload

from travel_plan import db
from travel_plan.car.cars import Car
from travel_plan.color import color_services


def get_names() -> List[str]:
    '''
    Gets a list of all of the car names.
    
    A car's name is a string made of it's plate, make, model, color, and location.
    
    :returns: a list of names or an empty list if no cars are found
    '''
    try:
        cars = db.session.query(Car).options(joinedload(Car.color)).all()
        return [c.name for c in cars]
    except Exception as e:
        print('excepton', e)
        return []


def get_id_from_plate(plate: str):
    '''
    Gets the id of a car with a given plate
    
    :param plate: the plate of a car
    :type plate: str
    :returns: the id of a car with the given plate or none if no matching car was found
    '''
    try:
        return db.session.query(Car.id).filter(Car.plate == plate).first()[0]
    except Exception as e:
        print(e)
        return None


def get_plates() -> Optional[List[str]]:
    '''
    Gets a list of all of the active cars.
    
    :returns: a list of plates for the active cars, or None if none are retrieved
    '''
    try:
        return [p[0] for p in db.session.query(Car.plate).filter(Car.active).order_by(Car.plate).all()]
    except:
        return []


def create_car(plate: str, make: str = None, model: str = None, color: str = None, location: str = None, active: bool = None) -> Car:
    '''
    Creates a car object and adds it to the database.
    
    Any parameters not supplied will be set to None.
    
    Government vehicles should presumably typically be set to active == True.
        
    :param plate: the car's license plate
    :type plate: str
    :param make: the car's make
    :type make: str
    :param model: the car's model
    :type model: str
    :param color: the car's color
    :type color: str
    :param location: the location where the car's typically left, ie. "The Valley", or "El Portal"
    :type location: str
    :param active: whether or not the car is generally available. It'd be considered
    "available" if it's generally in rotaiton to be used by travelers. Government
    vehicles will generally be set to active = True. Personal vehicles will generally 
    be set to active = False.
    :type active: bool
    :returns: the Car that was created
    '''
    
    color = color_services.add_if_not_present(color)

    car = Car(plate, make, model, color, location, active)

    db.session.add(car)
    db.session.commit()

    return car


def get_car(id: int = 0, plate: str = '') -> Optional[Car]:
    '''
    Gets a Car object given an id or plate.
    
    The intention is to provide the id OR the plate but not both.
    This avoids needing a "get_car_by_id" and "get_car_by_plate" functions.
    
    :param id: the id of a Car object that's to be retrieved
    :type id: int
    :param plate: the plate of a Car object that's to be retrieved
    :type plate: str
    :returns: a Car object with the supplied id or plate, or None if no car is found.
    '''
    
    if id:
        return db.session.query(Car).\
               options(joinedload(Car.color)).\
               filter(Car.id == id).\
               first()
    elif plate:
        return db.session.query(Car).\
               options(joinedload(Car.color)).\
               filter(Car.plate == plate).\
               first()
    else:
        return None
