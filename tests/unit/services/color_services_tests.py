import unittest.mock

from sqlalchemy.orm import Session


def test_color_services_get_names_success(db_session_w_info):
    from travel_plan.services import user_services

    locations, users, colors = db_session_w_info

    actual_names = user_services.get_names()

    expected_names = sorted([u['name'] for u in users])

    assert actual_names == expected_names
