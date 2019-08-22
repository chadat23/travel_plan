import unittest.mock
from typing import List

from sqlalchemy.orm import Session

from travel_plan.models.patrol_user_units import PatrolUserUnit


def test_patrol_services_get_names_success(db_session_w_patrols):
    from travel_plan.services import patrol_services

    patrols = db_session_w_patrols

    from travel_plan.models.patrols import Patrol
    patrols: List[Patrol] = patrol_services.get_all()
    patrollers: List[PatrolUserUnit] = patrols[0].patrollers
    color = patrollers[0].pack_color
    expected_names = sorted([u['start_date'] for u in patrols])

    assert actual_names == expected_names
