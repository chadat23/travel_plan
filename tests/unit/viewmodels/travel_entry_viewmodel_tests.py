from flask import Response

from tests.test_client import flask_app, client
from travel_plan.viewmodels.travel.travel_entry_viewmodel import TravelEntryViewModel

import unittest.mock


def test_travel_entry_vm_validate_end_before_start_success(form_data):
    # WITH: valid form data
    from datetime import datetime, timedelta

    # WHEN: DB calls are mocked and the exit date of is changed to
    # before the start date and the last day's plan is set to equal
    # the invalid exit date (to avoid a different error), and then
    # the vm is generated and validated.
    get_location_names, get_users, get_color_names, get_car_names = \
        _with_locaiton_names_users_color_names_car_names()

    start_date = datetime.strptime(form_data['entrydate'], '%Y-%m-%d')
    start_date = start_date - timedelta(days=5)
    start_date = datetime.strftime(start_date, '%Y-%m-%d')
    form_data['exitdate'] = start_date
    form_data['date2'] = start_date

    with get_location_names, get_users, get_color_names, get_car_names:
        with flask_app.test_request_context(path='/travel/entry', data=form_data):
            vm = TravelEntryViewModel()

    vm.validate()

    # THEN: the error message relays as such
    assert vm.error == "Your exit date can't be before your entry date."


def test_travel_entry_vm_validate_star_first_day_mismatch_success(form_data):
    # WITH: valid form data
    from datetime import datetime, timedelta

    # WHEN: DB calls are mocked and the date of the first day of the
    # itinerary is set 5 days before the start date and then the vm
    # is generated and validated.
    get_location_names, get_users, get_color_names, get_car_names = \
        _with_locaiton_names_users_color_names_car_names()

    start_date = datetime.strptime(form_data['entrydate'], '%Y-%m-%d')
    start_date = start_date - timedelta(days=5)
    start_date = datetime.strftime(start_date, '%Y-%m-%d')
    form_data['date0'] = start_date

    with get_location_names, get_users, get_color_names, get_car_names:
        with flask_app.test_request_context(path='/travel/entry', data=form_data):
            vm = TravelEntryViewModel()

    vm.validate()

    # THEN: the error message dictates that there's a date mismatch
    assert 'should start on your entry date.' in vm.error


def test_travel_entry_vm_validate_end_last_day_mismatch_success(form_data):
    # WITH: valid form data
    from datetime import datetime, timedelta

    # WHEN: DB calls are mocked and the date of the last day of the
    # itinerary is set 5 days after the exit date and then the vm
    # is generated and validated.
    get_location_names, get_users, get_color_names, get_car_names = \
        _with_locaiton_names_users_color_names_car_names()

    exit_date = datetime.strptime(form_data['exitdate'], '%Y-%m-%d')
    exit_date = exit_date + timedelta(days=5)
    exit_date = datetime.strftime(exit_date, '%Y-%m-%d')
    form_data['date2'] = exit_date

    with get_location_names, get_users, get_color_names, get_car_names:
        with flask_app.test_request_context(path='/travel/entry', data=form_data):
            vm = TravelEntryViewModel()

    vm.validate()

    # THEN: the error message dictates that there's a date mismatch.
    assert 'should end on your exit date.' in vm.error


def test_travel_entry_vm_entry_exit_date_success(form_data):
    # WITH: valid form data
    get_location_names, get_users, get_color_names, get_car_names = _with_locaiton_names_users_color_names_car_names()

    # WHEN: the DB calls are mocked and then the vm is generated.
    with get_location_names, get_users, get_color_names, get_car_names:
        with flask_app.test_request_context(path='/travel/entry', data=form_data):
            vm = TravelEntryViewModel()

    # THEN: all of the data in the form should be properly represented in the vm.
    assert vm.entry_date == form_data['entrydate']
    assert vm.entry_point == form_data['entrypoint']
    assert vm.exit_date == form_data['exitdate']
    assert vm.exit_point == form_data['exitpoint']
    # assert vm.tracked == good_form_data['tracked']
    assert vm.tracked is True
    assert vm.plb == form_data['plb']

    assert vm.patrollers[0]['name'] == form_data['name0']
    assert vm.patrollers[0]['pack_color'] == form_data['packcolor0']
    assert vm.patrollers[0]['tent_color'] == form_data['tentcolor0']
    assert vm.patrollers[0]['fly_color'] == form_data['flycolor0']
    assert vm.patrollers[0]['s'] == form_data['s0']
    assert vm.patrollers[0]['p'] == form_data['p0']
    assert vm.patrollers[0]['cr'] == form_data['cr0']
    assert vm.patrollers[0]['c'] == form_data['c0']
    assert vm.patrollers[0]['ts'] == form_data['ts0']
    assert vm.patrollers[0]['tf'] == form_data['tf0']
    assert vm.patrollers[0]['e'] == form_data['e0']
    assert vm.patrollers[0]['ic'] == form_data['ic0']
    assert vm.patrollers[1]['name'] == form_data['name1']
    assert vm.patrollers[1]['pack_color'] == form_data['packcolor1']
    assert vm.patrollers[1]['tent_color'] == form_data['tentcolor1']
    assert vm.patrollers[1]['fly_color'] == form_data['flycolor1']
    assert vm.patrollers[1]['s'] == form_data['s1']
    assert vm.patrollers[1]['p'] == form_data['p1']
    assert vm.patrollers[1]['cr'] == form_data['cr1']
    assert vm.patrollers[1]['c'] == form_data['c1']
    assert vm.patrollers[1]['ts'] == form_data['ts1']
    assert vm.patrollers[1]['tf'] == form_data['tf1']
    assert vm.patrollers[1]['e'] == form_data['e1']
    assert vm.patrollers[1]['ic'] == form_data['ic1']

    assert vm.day_plans[0]['date'] == form_data['date0']
    assert vm.day_plans[0]['start'] == form_data['start0']
    assert vm.day_plans[0]['end'] == form_data['end0']
    assert vm.day_plans[0]['route'] == form_data['route0']
    assert vm.day_plans[0]['mode'] == form_data['mode0']
    assert vm.day_plans[1]['date'] == form_data['date1']
    assert vm.day_plans[1]['start'] == form_data['start1']
    assert vm.day_plans[1]['end'] == form_data['end1']
    assert vm.day_plans[1]['route'] == form_data['route1']
    assert vm.day_plans[1]['mode'] == form_data['mode1']
    assert vm.day_plans[2]['date'] == form_data['date2']
    assert vm.day_plans[2]['start'] == form_data['start2']
    assert vm.day_plans[2]['end'] == form_data['end2']
    assert vm.day_plans[2]['route'] == form_data['route2']
    assert vm.day_plans[2]['mode'] == form_data['mode2']

    assert vm.car_plate == form_data['carplate']
    assert vm.car_make == form_data['carmake']
    assert vm.car_model == form_data['carmodel']
    assert vm.car_color == form_data['carcolor']
    assert vm.car_location == form_data['carlocation']

    assert vm.bivy_gear == 'on'
    assert vm.compass == 'on'
    assert vm.first_aid_kit == 'on'
    assert vm.flagging == 'on'
    assert vm.flare == 'on'
    assert vm.flashlight == 'on'
    assert vm.gps == 'on'
    assert vm.head_lamp == 'on'
    assert vm.helmet == 'on'
    assert vm.ice_axe == 'on'
    assert vm.map == 'on'
    assert vm.matches == 'on'
    assert vm.probe_pole == 'on'
    assert vm.radio == 'on'
    assert vm.rope == 'on'
    assert vm.shovel == 'on'
    assert vm.signal_mirror == 'on'
    assert vm.space_blanket == 'on'
    assert vm.spare_battery == 'on'
    assert vm.tent == 'on'
    assert vm.whistle == 'on'

    assert vm.days_of_food == form_data['daysoffood']
    assert vm.radio_monitor_time == form_data['radiomonitortime']
    # assert vm.off_trail_travel == good_form_data['offtrailtravel']
    assert vm.off_trail_travel is True
    # Need off trail travel map
    assert vm.cell_number == form_data['cellnumber']
    assert vm.satellite_number == form_data['satellitenumber']

    assert vm.contact_email0 == form_data['contactemail0']
    assert vm.contact_work0 == form_data['contactwork0']
    assert vm.contact_home0 == form_data['contacthome0']
    assert vm.contact_cell0 == form_data['contactcell0']
    assert vm.contact_email1 == form_data['contactemail1']
    assert vm.contact_work1 == form_data['contactwork1']
    assert vm.contact_home1 == form_data['contacthome1']
    assert vm.contact_cell1 == form_data['contactcell1']

    assert vm.s_avg == form_data['savg']
    assert vm.p_avg == form_data['pavg']
    assert vm.cr_avg == form_data['cravg']
    assert vm.c_avg == form_data['cavg']
    assert vm.ts_avg == form_data['tsavg']
    assert vm.tf_avg == form_data['tfavg']
    assert vm.e_avg == form_data['eavg']
    assert vm.ic_avg == form_data['icavg']

    assert vm.gar_avg == form_data['garavg']
    assert vm.mitigated_avg == form_data['mitigatedavg']
    assert vm.gar_mitigations == form_data['garmitigations']
    assert vm.notes == form_data['notes']


def _with_locaiton_names_users_color_names_car_names():
    target = 'travel_plan.services.location_services.get_names'
    get_location_names = unittest.mock.patch(target, return_value=None)
    target = 'travel_plan.services.user_services.get_users'
    get_users = unittest.mock.patch(target, return_value=None)
    target = 'travel_plan.services.color_services.get_names'
    get_color_names = unittest.mock.patch(target, return_value=None)
    target = 'travel_plan.services.car_services.get_names'
    get_car_names = unittest.mock.patch(target, return_value=None)

    return get_location_names, get_users, get_color_names, get_car_names
