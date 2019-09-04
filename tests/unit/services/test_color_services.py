import unittest.mock

from sqlalchemy.orm import Session


def test_color_services_get_names_success(db_session_w_info):
    from travel_plan.services import color_services

    locations, users, colors, cars = db_session_w_info

    actual_names = color_services.get_names()

    expected_names = sorted(colors)

    assert actual_names == expected_names
