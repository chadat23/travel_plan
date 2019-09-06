import unittest.mock
from typing import List

import pytest
from sqlalchemy.orm import Session

from travel_plan.models.travel_user_units import TravelUserUnit


@pytest.mark.xfail
def test_travel_services_get_names_success(db_session_w_travel_info):
    from travel_plan.models.travels import Travel
    from travel_plan.services import travel_services

    expected_travels = db_session_w_travel_info
    actual_travels = []

    for travel in expected_travels:
        p = travel['travel']
        actual_travels.append(
            travel_services.add_travel(p['start_date'], p['entry_point'], p['end_date'], p['exit_point'],
                                       p['tracked'], p['plb'], p['trip_leader_name'],
                                       travel['traveler_units'], p['car'], p['car_locaton']
                                       ))

    for actual, expected in zip(actual_travels, expected_travels):
        assert isinstance(actual, Travel)
        assert actual.start_date.strftime("%Y-%m-%d") == expected['travel']['start_date']
        # assert actual.entry_point.name == expected['travel']['entry_point']
