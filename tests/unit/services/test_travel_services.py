import unittest.mock
from typing import List

import pytest
from sqlalchemy.orm import Session

from travel_plan.models.patrol_user_units import PatrolUserUnit


def test_patrol_services_get_names_success(db_session_w_patrol_info):
    import unittest.mock
    from unittest.mock import Mock

    from travel_plan.models.patrols import Patrol
    from travel_plan.services import travel_services

    expected_patrols = db_session_w_patrol_info
    actual_patrols = []

    m = Mock()
    m.side_effect = [1, 2, 2, 3, 3, 1]
    target = 'travel_plan.serviceslocation_services.get_id_from_name'
    get_location_id = unittest.mock.patch(target, return_value = m())

    for patrol in expected_patrols:
        p = patrol['patrol']
        actual_patrols.append(
            travel_services.create_plan(p['start_date'], p['entry_point'], p['end_date'], p['exit_point'],
                                        p['tracked'], p['plb'], 
                                        patrol['patroller_units'], patrol['day_plans'],
                                        p['car'], p['car_locaton']
                                        p['trip_leader_name'],
            
            )

    for actual, expected in zip(actual_patrols, expected_patrols):
        assert isinstance(actual, Patrol)
        assert actual.start_date.strftime("%Y-%m-%d") == expected['patrol']['start_date']
        # assert actual.entry_point.name == expected['patrol']['entry_point']
