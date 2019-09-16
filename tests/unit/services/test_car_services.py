from sqlalchemy.orm import Session


def test_car_services_get_names(db_session_w_info):
    from travel_plan.models.cars import Car
    from travel_plan.services import car_services

    locations, users, colors, cars = db_session_w_info

    names = car_services.get_names()
    assert cars[0]['plate'] in names[2]
    assert cars[1]['plate'] in names[1]


def test_car_services_get_id_from_plate(db_session_w_info):
    from travel_plan.services import car_services

    locations, users, colors, cars = db_session_w_info

    for i, car in enumerate(cars):
        id = car_services.get_id_from_plate(car['plate'])
        assert id == i + 1


def test_car_services_get_plates(db_session_w_info):
    from travel_plan.models.cars import Car
    from travel_plan.services import car_services

    locations, users, colors, cars = db_session_w_info

    plates = car_services.get_plates()
    assert cars[0]['plate'] in plates[0]
    assert cars[1]['plate'] in plates[1]


def test_car_services_create_car(db_session_w_info):
    import unittest.mock

    from travel_plan.models.cars import Car
    from travel_plan.services import car_services

    locations, users, colors, cars = db_session_w_info

    plate = '123-321'
    make = 'Ford'
    model = 'Vroom Queen'
    color = 'White'
    location = 'The Complex'
    active = False

    target = 'travel_plan.services.color_services.add_if_not_present'
    test_color = unittest.mock.patch(target, return_value='White')
    with test_color:
        car = car_services.create_car(plate, make, model, color, location, active)

    assert car_services.get_id_from_plate(plate) == len(cars) + 1
    assert isinstance(car, Car)
    assert car.plate == plate
    assert car.make == make
    assert car.model == model
    assert car.color == color
    assert car.location == location
    assert not car.active
