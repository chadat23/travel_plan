import unittest.mock

from sqlalchemy.orm import Session


def test_patrol_services_get_names_success(db_session_w_patrols):
    from travel_plan.services import user_services

    locations, users, colors = db_session_w_patrols

    actual_names = user_services.get_names()

    expected_names = sorted([u['name'] for u in users])

    assert actual_names == expected_names
