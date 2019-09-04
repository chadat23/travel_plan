import unittest.mock

from sqlalchemy.orm import Session


def test_color_services_get_names_success(db_session_w_info):
    from travel_plan.services import color_services

    locations, users, colors, cars = db_session_w_info

    actual_names = color_services.get_names()

    expected_names = sorted(colors)

    assert actual_names == expected_names


def test_color_services_is_present_success(db_session_w_info):
    from travel_plan.services import color_services

    locations, users, colors, cars = db_session_w_info

    assert color_services.is_present(colors[0])
    

def test_color_services_is_present_not_success(db_session_w_info):
    from travel_plan.services import color_services

    locations, users, colors, cars = db_session_w_info

    assert not color_services.is_present('Nope')


def test_color_services_add_success(db_session_w_info):
    from travel_plan.services import color_services

    locations, users, colors, cars = db_session_w_info

    color = 'Blart'

    assert not color_services.is_present(color)

    assert color_services.add(color)

    assert color_services.is_present(color)


def test_color_services_add_if_not_present_success(db_session_w_info):
    from travel_plan.services import color_services

    locations, users, colors, cars = db_session_w_info

    color = 'Blart'

    assert not color_services.is_present(color)

    assert color_services.add_if_not_present(color)

    assert color_services.is_present(color)


def test_color_services_add_if_not_present_not_success(db_session_w_info):
    from travel_plan.services import color_services

    locations, users, colors, cars = db_session_w_info

    color = colors[0]

    assert color_services.is_present(color)

    assert not color_services.add_if_not_present(color)
