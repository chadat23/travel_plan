import unittest.mock
from typing import List

import pytest
from sqlalchemy.orm import Session

from travel_plan.models.travel_user_units import TravelUserUnit


def test_travel_services_create_plan_success(db_session_w_travel_info):
    import unittest.mock
    from unittest.mock import Mock

    from travel_plan.models.travels import Travel
    from travel_plan.services import travel_services

    expected_travels = db_session_w_travel_info
    actual_travels = []

    m = Mock()
    m.side_effect = [1, 2, 2, 3, 3, 1]
    target = 'travel_plan.services.location_services.get_id_from_name'
    get_location_id = unittest.mock.patch(target, return_value=m())
    m.side_effect = [1, 2, 2, 3, 3, 1]
    target = 'travel_plan.services.car_services.get_id_from_plate'
    get_car_id = unittest.mock.patch(target, return_value=m())
    target = 'travel_plan.services.user_services.get_id_from_name'
    get_user_id = unittest.mock.patch(target, return_value=1)

    with get_location_id, get_car_id, get_user_id:
        for travel in expected_travels:
            p = travel['travel']
            actual_travels.append(
                travel_services.create_plan(p['start_date'], p['entry_point'], p['end_date'], p['exit_point'],
                                            p['tracked'], p['plb'], p['trip_leader_name'],
                                            travel['traveler_units'], travel['day_plans'],
                                            p['car_plate'], p['car_make'], p['car_model'], p['car_color'],
                                            p['car_locaton'],
                                            p['bivy_gear'] == 'on',
                                            p['compass'] == 'on',
                                            p['first_aid_kit'] == 'on',
                                            p['flagging'] == 'on',
                                            p['flare'] == 'on',
                                            p['flashlight'] == 'on',
                                            p['gps'] == 'on',
                                            p['head_lamp'] == 'on',
                                            p['helmet'] == 'on',
                                            p['ice_axe'] == 'on',
                                            p['map'] == 'on',
                                            p['matches'] == 'on',
                                            p['probe_pole'] == 'on',
                                            p['radio'] == 'on',
                                            p['rope'] == 'on',
                                            p['shovel'] == 'on',
                                            p['signal_mirror'] == 'on',
                                            p['space_blanket'] == 'on',
                                            p['spare_battery'] == 'on',
                                            p['tent'] == 'on',
                                            p['whistle'] == 'on',
                                            p['days_of_food'], p['weapon'], p['radio_monitor_time'],
                                            p['off_trail_travel'],
                                            p['cell_number'], p['satellite_number'],
                                            travel['contacts'],
                                            p['gar_avg'], p['mitigated_gar'], p['gar_mitigations'],
                                            p['notes'],
                                            )
            )

    for actual, expected in zip(actual_travels, expected_travels):
        assert isinstance(actual, int)
        # assert actual.start_date.strftime("%Y-%m-%d") == expected['travel']['start_date']
        # assert actual.entry_point.name == expected['travel']['entry_point']
