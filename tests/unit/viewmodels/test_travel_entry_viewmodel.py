from travel_plan.viewmodels.travel.travel_entry_viewmodel import TravelEntryViewModel

import unittest.mock


def test_travel_entry_vm_validate_end_before_start_success(app_w_db, form_data):
    # WITH: valid form data
    from datetime import datetime, timedelta

    # WHEN: DB calls are mocked and the exit date of is changed to
    # before the start date and the last day's plan is set to equal
    # the invalid exit date (to avoid a different error), and then
    # the vm is generated and validated.
    get_location_names, get_users, get_color_names, get_car_names = \
        _with_locaiton_names_users_color_names_car_names()

    start_date = datetime.strptime(form_data['startdate'], '%Y-%m-%d')
    start_date = start_date - timedelta(days=5)
    start_date = datetime.strftime(start_date, '%Y-%m-%d')
    form_data['enddate'] = start_date
    form_data['date2'] = start_date

    with get_location_names, get_users, get_color_names, get_car_names:
        with app_w_db.test_request_context(path='/travel/entry', data=form_data):
            vm = TravelEntryViewModel()

    vm.validate()

    # THEN: the error message relays as such
    assert vm.error == "Your exit date can't be before your entry date."


def test_travel_entry_vm_validate_star_first_day_mismatch_success(app_w_db, form_data):
    # WITH: valid form data
    from datetime import datetime, timedelta

    # WHEN: DB calls are mocked and the date of the first day of the
    # itinerary is set 5 days before the start date and then the vm
    # is generated and validated.
    get_location_names, get_users, get_color_names, get_car_names = \
        _with_locaiton_names_users_color_names_car_names()

    start_date = datetime.strptime(form_data['startdate'], '%Y-%m-%d')
    start_date = start_date - timedelta(days=5)
    start_date = datetime.strftime(start_date, '%Y-%m-%d')
    form_data['date0'] = start_date

    with get_location_names, get_users, get_color_names, get_car_names:
        with app_w_db.test_request_context(path='/travel/entry', data=form_data):
            vm = TravelEntryViewModel()

    vm.validate()

    # THEN: the error message dictates that there's a date mismatch
    assert 'should start on your entry date.' in vm.error


def test_travel_entry_vm_validate_end_last_day_mismatch_success(app_w_db, form_data):
    # WITH: valid form data
    from datetime import datetime, timedelta

    # WHEN: DB calls are mocked and the date of the last day of the
    # itinerary is set 5 days after the exit date and then the vm
    # is generated and validated.
    get_location_names, get_users, get_color_names, get_car_names = \
        _with_locaiton_names_users_color_names_car_names()

    end_date = datetime.strptime(form_data['enddate'], '%Y-%m-%d')
    end_date = end_date + timedelta(days=5)
    end_date = datetime.strftime(end_date, '%Y-%m-%d')
    form_data['date2'] = end_date

    with get_location_names, get_users, get_color_names, get_car_names:
        with app_w_db.test_request_context(path='/travel/entry', data=form_data):
            vm = TravelEntryViewModel()

    vm.validate()

    # THEN: the error message dictates that there's a date mismatch.
    assert 'should end on your exit date.' in vm.error


def test_travel_entry_vm_validate_only_only_off_trail_travel_selected_success(app_w_db, form_data):
    # WITH:
    get_location_names, get_users, get_color_names, get_car_names = _with_locaiton_names_users_color_names_car_names()

    form_data['offtrailtravel'] = 'yes'

    # WHEN: the DB calls are mocked and then the vm is generated.
    with get_location_names, get_users, get_color_names, get_car_names:
        with app_w_db.test_request_context(path='/travel/entry', data=form_data):
            vm = TravelEntryViewModel()

    vm.validate()

    assert 'Either you should' in vm.error


def test_travel_entry_vm_convert_empty_strings_to_none(app_w_db, form_data_w_nones):
    get_location_names, get_users, get_color_names, get_car_names = _with_locaiton_names_users_color_names_car_names()

    # WHEN: the DB calls are mocked and then the vm is generated.
    with get_location_names, get_users, get_color_names, get_car_names:
        with app_w_db.test_request_context(path='/travel/entry', data=form_data_w_nones):
            vm = TravelEntryViewModel()

    assert vm.plb == ''

    vm.convert_empty_strings_to_none()

    assert vm.plb == None


def test_travel_entry_vm_entry_end_date_success(app_w_db, form_data):
    # WITH: valid form data
    get_location_names, get_users, get_color_names, get_car_names = _with_locaiton_names_users_color_names_car_names()

    # WHEN: the DB calls are mocked and then the vm is generated.
    with get_location_names, get_users, get_color_names, get_car_names:
        with app_w_db.test_request_context(path='/travel/entry', data=form_data):
            vm = TravelEntryViewModel()

    # THEN: all of the data in the form should be properly represented in the vm.
    assert vm.start_date == form_data['startdate']
    assert vm.entry_point == form_data['entrypoint']
    assert vm.end_date == form_data['enddate']
    assert vm.exit_point == form_data['exitpoint']
    # assert vm.tracked == form_data['tracked']
    assert vm.tracked is True
    assert vm.plb == form_data['plb']

    assert vm.trip_leader_name == form_data['travelername0']

    assert vm.travelers[0]['traveler_name'] == form_data['travelername0']
    assert vm.travelers[0]['pack_color'] == form_data['packcolor0']
    assert vm.travelers[0]['tent_color'] == form_data['tentcolor0']
    assert vm.travelers[0]['fly_color'] == form_data['flycolor0']
    assert vm.travelers[0]['supervision'] == form_data['supervision0']
    assert vm.travelers[0]['planning'] == form_data['planning0']
    assert vm.travelers[0]['contingency'] == form_data['contingency0']
    assert vm.travelers[0]['comms'] == form_data['comms0']
    assert vm.travelers[0]['team_selection'] == form_data['teamselection0']
    assert vm.travelers[0]['fitness'] == form_data['fitness0']
    assert vm.travelers[0]['env'] == form_data['env0']
    assert vm.travelers[0]['complexity'] == form_data['complexity0']
    assert vm.travelers[0]['total'] == form_data['total0']
    assert vm.travelers[1]['traveler_name'] == form_data['travelername1']
    assert vm.travelers[1]['pack_color'] == form_data['packcolor1']
    assert vm.travelers[1]['tent_color'] == form_data['tentcolor1']
    assert vm.travelers[1]['fly_color'] == form_data['flycolor1']
    assert vm.travelers[1]['supervision'] == form_data['supervision1']
    assert vm.travelers[1]['planning'] == form_data['planning1']
    assert vm.travelers[1]['contingency'] == form_data['contingency1']
    assert vm.travelers[1]['comms'] == form_data['comms1']
    assert vm.travelers[1]['team_selection'] == form_data['teamselection1']
    assert vm.travelers[1]['fitness'] == form_data['fitness1']
    assert vm.travelers[1]['env'] == form_data['env1']
    assert vm.travelers[1]['complexity'] == form_data['complexity1']
    assert vm.travelers[1]['total'] == form_data['total1']

    assert vm.day_plans[0]['date'] == form_data['date0']
    assert vm.day_plans[0]['starting_point'] == form_data['startingpoint0']
    assert vm.day_plans[0]['ending_point'] == form_data['endingpoint0']
    assert vm.day_plans[0]['route'] == form_data['route0']
    assert vm.day_plans[0]['mode'] == form_data['mode0']
    assert vm.day_plans[1]['date'] == form_data['date1']
    assert vm.day_plans[1]['starting_point'] == form_data['startingpoint1']
    assert vm.day_plans[1]['ending_point'] == form_data['endingpoint1']
    assert vm.day_plans[1]['route'] == form_data['route1']
    assert vm.day_plans[1]['mode'] == form_data['mode1']
    assert vm.day_plans[2]['date'] == form_data['date2']
    assert vm.day_plans[2]['starting_point'] == form_data['startingpoint2']
    assert vm.day_plans[2]['ending_point'] == form_data['endingpoint2']
    assert vm.day_plans[2]['route'] == form_data['route2']
    assert vm.day_plans[2]['mode'] == form_data['mode2']

    assert vm.car_plate == form_data['carplate']
    assert vm.car_make == form_data['carmake']
    assert vm.car_model == form_data['carmodel']
    assert vm.car_color == form_data['carcolor']
    assert vm.car_location == form_data['carlocation']

    # assert vm.bivy_gear == 'on'
    assert vm.bivy_gear is True
    assert vm.compass is True
    assert vm.first_aid_kit is True
    assert vm.flagging is True
    assert vm.flare is True
    assert vm.flashlight
    assert vm.gps
    assert vm.head_lamp is True
    assert vm.helmet is True
    assert vm.ice_axe is True
    assert vm.map is True
    assert vm.matches is True
    assert vm.probe_pole is True
    assert vm.radio is True
    assert vm.rope is True
    assert vm.shovel is True
    assert vm.signal_mirror is True
    assert vm.space_blanket is True
    assert vm.spare_battery is True
    assert vm.tent is True
    assert vm.whistle is True

    assert vm.days_of_food == form_data['daysoffood']
    assert vm.radio_monitor_time == form_data['radiomonitortime']
    # assert vm.off_trail_travel == good_form_data['offtrailtravel']
    assert vm.off_trail_travel is False
    # Need off trail travel map
    assert vm.cell_number == form_data['cellnumber']
    assert vm.satellite_number == form_data['satellitenumber']

    for i, c in enumerate(vm.contacts):
        assert c['contact_name'] == form_data['contactname' + str(i)]
        assert c['contact_email'] == form_data['contactemail' + str(i)]

    assert vm.gar_avg == form_data['garavg']
    assert vm.mitigated_gar == form_data['mitigatedgar']
    assert vm.gar_mitigations == form_data['garmitigations']
    assert vm.notes == form_data['notes']


def _with_locaiton_names_users_color_names_car_names():
    target = 'travel_plan.location.location_services.get_names'
    get_location_names = unittest.mock.patch(target, return_value=None)
    target = 'travel_plan.user.user_services.get_users'
    get_users = unittest.mock.patch(target, return_value=None)
    target = 'travel_plan.color.color_services.get_names'
    get_color_names = unittest.mock.patch(target, return_value=None)
    target = 'travel_plan.car.car_services.get_names'
    get_car_names = unittest.mock.patch(target, return_value=None)

    return get_location_names, get_users, get_color_names, get_car_names
