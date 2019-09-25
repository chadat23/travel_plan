def test_car_services_get_names(app_w_db, cars):
    from travel_plan.services import car_services

    names = car_services.get_names()

    for c, n in zip(cars, names):
        assert c['plate'] in n


def test_car_services_get_id_from_plate(app_w_db, cars):
    from travel_plan.services import car_services

    for i, car in enumerate(cars):
        id = car_services.get_id_from_plate(car['plate'])
        assert id == i + 1


def test_car_services_get_plates(app_w_db, cars):
    from travel_plan.services import car_services

    plates = car_services.get_plates()
    assert cars[0]['plate'] in plates[0]
    assert cars[1]['plate'] in plates[1]


def test_car_services_create_car(app_w_db, cars):
    import unittest.mock

    from travel_plan.models.cars import Car
    from travel_plan.services import car_services

    # locations, users, colors, cars = db_session_w_info

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

    car = car_services.get_car(id=car.id)

    assert car_services.get_id_from_plate(plate) == len(cars) + 1
    assert isinstance(car, Car)
    assert car.plate == plate
    assert car.make == make
    assert car.model == model
    assert car.color.name == color
    assert car.location == location
    assert not car.active
