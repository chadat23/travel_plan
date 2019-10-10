def test_travel_services_create_plan_success(app_w_empty_db, travels):
    import unittest.mock
    from unittest.mock import Mock

    from travel_plan.travel import travel_services

    expected_travels = travels
    actual_travels = []

    m = Mock()
    m.side_effect = [1, 2, 2, 3, 3, 1]
    target = 'travel_plan.location.location_services.get_id_by_name'
    get_location_id = unittest.mock.patch(target, return_value=m())
    m.side_effect = [1, 2, 2, 3, 3, 1]
    target = 'travel_plan.car.car_services.get_id_by_plate'
    get_car_id = unittest.mock.patch(target, return_value=m())
    target = 'travel_plan.user.user_services.get_id_by_name'
    get_user_id = unittest.mock.patch(target, return_value=1)

    with get_location_id, get_car_id, get_user_id:
        for travel in expected_travels:
            p = travel['travel']
            actual_travels.append(
                travel_services.create_plan(p['start_date'], p['entry_point'], p['end_date'], p['exit_point'],
                                            p['tracked'], p['plb'], p['trip_leader_name'],
                                            travel['traveler_units'], travel['day_plans'],
                                            p['car_plate'], p['car_make'], p['car_model'], p['car_color'],
                                            p['car_location'],
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
                                            p['notes'], travel['files']
                                            )
            )

    for actual, expected in zip(actual_travels, expected_travels):
        assert isinstance(actual, int)


def test_travel_services_create_plan_success_w_nones(app_w_empty_db, travels_w_nones):
    import unittest.mock
    from unittest.mock import Mock

    from travel_plan.travel import travel_services

    expected_travels = travels_w_nones
    actual_travels = []

    m = Mock()
    m.side_effect = [1, 2, 2, 3, 3, 1]
    target = 'travel_plan.location.location_services.get_id_by_name'
    get_location_id = unittest.mock.patch(target, return_value=m())
    m.side_effect = [1, 2, 2, 3, 3, 1]
    target = 'travel_plan.car.car_services.get_id_by_plate'
    get_car_id = unittest.mock.patch(target, return_value=m())
    target = 'travel_plan.user.user_services.get_id_by_name'
    get_user_id = unittest.mock.patch(target, return_value=1)

    with get_location_id, get_car_id, get_user_id:
        for travel in expected_travels:
            p = travel['travel']
            actual_travels.append(
                travel_services.create_plan(p['start_date'], p['entry_point'], p['end_date'], p['exit_point'],
                                            p['tracked'], p['plb'], p['trip_leader_name'],
                                            travel['traveler_units'], travel['day_plans'],
                                            p['car_plate'], p['car_make'], p['car_model'], p['car_color'],
                                            p['car_location'],
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
                                            p['notes'], travel['files']
                                            )
            )

    for actual, expected in zip(actual_travels, expected_travels):
        assert isinstance(actual, int)
