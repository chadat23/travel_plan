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
    target = 'travel_plan.services.location_services.get_id_from_name'
    get_location_id = unittest.mock.patch(target, return_value=m())
    m.side_effect = [1, 2, 2, 3, 3, 1]
    target = 'travel_plan.services.car_services.get_id_from_plate'
    get_car_id = unittest.mock.patch(target, return_value=m())

    with get_location_id, get_car_id:
        for patrol in expected_patrols:
            p = patrol['patrol']
            actual_patrols.append(
                travel_services.create_plan(p['start_date'], p['entry_point'], p['end_date'], p['exit_point'],
                                            p['tracked'], p['plb'],
                                            patrol['patroller_units'], patrol['day_plans'],
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
                                            )
            )

    for actual, expected in zip(actual_patrols, expected_patrols):
        assert isinstance(actual, Patrol)
        assert actual.start_date.strftime("%Y-%m-%d") == expected['patrol']['start_date']
        # assert actual.entry_point.name == expected['patrol']['entry_point']
