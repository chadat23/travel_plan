import unittest.mock
from typing import List

from sqlalchemy.orm import Session

from travel_plan.models.patrol_user_units import PatrolUserUnit


def test_patrol_services_get_names_success(db_session_w_patrol_info):
    from travel_plan.models.patrols import Patrol
    from travel_plan.services import patrol_services

    patrols = db_session_w_patrol_info
    
    for patrol in patrols:
        p = patrol['patrol']
        patrol_services.add_patrol(p['start_date'], p['entry_point'], p['end_date'], p['exit_point'],
                                   p['tracked'], p['plb'], p['trip_leader_name'],
                                   patrol['users']
                                   )

    print('hello')

    assert actual_names == expected_names
