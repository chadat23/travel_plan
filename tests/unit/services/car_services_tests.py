from sqlalchemy.orm import Session


def test_car_services_get_names(db_session_w_info):
    from travel_plan.models.cars import Car
    from travel_plan.services import car_services

    locations, users, colors, cars = db_session_w_info

    names = car_services.get_names()
    assert cars[0]['plate'] in names[2]
    assert cars[1]['plate'] in names[1]


def test_car_services_get_id_from_plat(db_session_w_info):
    from travel_plan.services import car_services

    locations, users, colors, cars = db_session_w_info

    for i, car in enumerate(cars):
        id = car_services.get_id_from_plate(car['plate'])
        assert id == i+1
