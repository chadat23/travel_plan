import unittest.mock
from typing import List

from sqlalchemy.orm import Session

from travel_plan.models.patrol_user_units import PatrolUserUnit


def test_patrol_services_get_names_success(db_session_w_patrol_info):
    from travel_plan.models.patrols import Patrol
    from travel_plan.services import patrol_services

    expected_patrols = db_session_w_patrol_info
    actual_patrols = []

    for patrol in expected_patrols:
        p = patrol['patrol']
        actual_patrols.append(
            patrol_services.add_patrol(p['start_date'], p['entry_point'], p['end_date'], p['exit_point'],
                                       p['tracked'], p['plb'], p['trip_leader_name'],
                                       patrol['patroller_units'], p['car'], p['car_locaton']
                                       ))

    for actual, expected in zip(actual_patrols, expected_patrols):
        assert isinstance(actual, Patrol)
        assert actual.start_date.strftime("%Y-%m-%d") == expected['patrol']['start_date']
        # assert actual.entry_point.name == expected['patrol']['entry_point']
