from flask import Response

from tests.test_client import flask_app, client
from travel_plan.viewmodels.travel.travel_entry_viewmodel import TravelEntryViewModel

import unittest.mock


def test_travel_entry_vm_entry_exit_date_success(good_form_data):
    target = 'travel_plan.services.location_services.get_names'
    get_location_names = unittest.mock.patch(target, return_value=None)
    target = 'travel_plan.services.user_services.get_users'
    get_users = unittest.mock.patch(target, return_value=None)
    target = 'travel_plan.services.color_services.get_names'
    get_color_names = unittest.mock.patch(target, return_value=None)
    target = 'travel_plan.services.car_services.get_names'
    get_car_names = unittest.mock.patch(target, return_value=None)

    with get_location_names, get_users, get_color_names, get_car_names:
        with flask_app.test_request_context(path='/travel/entry', data=good_form_data):
            vm = TravelEntryViewModel()

    assert vm.entry_date == good_form_data['entrydate']
    assert vm.entry_point == good_form_data['entrypoint']
    assert vm.exit_date == good_form_data['exitdate']
    assert vm.exit_point == good_form_data['exitpoint']
    # assert vm.tracked == good_form_data['tracked']
    assert vm.tracked is True
    assert vm.plb == good_form_data['plb']

    assert vm.patrollers[0]['name'] == good_form_data['name0']
    assert vm.patrollers[0]['pack_color'] == good_form_data['packcolor0']
    assert vm.patrollers[0]['tent_color'] == good_form_data['tentcolor0']
    assert vm.patrollers[0]['fly_color'] == good_form_data['flycolor0']
    assert vm.patrollers[0]['s'] == good_form_data['s0']
    assert vm.patrollers[0]['p'] == good_form_data['p0']
    assert vm.patrollers[0]['cr'] == good_form_data['cr0']
    assert vm.patrollers[0]['c'] == good_form_data['c0']
    assert vm.patrollers[0]['ts'] == good_form_data['ts0']
    assert vm.patrollers[0]['tf'] == good_form_data['tf0']
    assert vm.patrollers[0]['e'] == good_form_data['e0']
    assert vm.patrollers[0]['ic'] == good_form_data['ic0']
    assert vm.patrollers[1]['name'] == good_form_data['name1']
    assert vm.patrollers[1]['pack_color'] == good_form_data['packcolor1']
    assert vm.patrollers[1]['tent_color'] == good_form_data['tentcolor1']
    assert vm.patrollers[1]['fly_color'] == good_form_data['flycolor1']
    assert vm.patrollers[1]['s'] == good_form_data['s1']
    assert vm.patrollers[1]['p'] == good_form_data['p1']
    assert vm.patrollers[1]['cr'] == good_form_data['cr1']
    assert vm.patrollers[1]['c'] == good_form_data['c1']
    assert vm.patrollers[1]['ts'] == good_form_data['ts1']
    assert vm.patrollers[1]['tf'] == good_form_data['tf1']
    assert vm.patrollers[1]['e'] == good_form_data['e1']
    assert vm.patrollers[1]['ic'] == good_form_data['ic1']

    assert vm.day_plans[0]['date'] == good_form_data['date0']
    assert vm.day_plans[0]['start'] == good_form_data['start0']
    assert vm.day_plans[0]['end'] == good_form_data['end0']
    assert vm.day_plans[0]['route'] == good_form_data['route0']
    assert vm.day_plans[0]['mode'] == good_form_data['mode0']
    assert vm.day_plans[1]['date'] == good_form_data['date1']
    assert vm.day_plans[1]['start'] == good_form_data['start1']
    assert vm.day_plans[1]['end'] == good_form_data['end1']
    assert vm.day_plans[1]['route'] == good_form_data['route1']
    assert vm.day_plans[1]['mode'] == good_form_data['mode1']
    assert vm.day_plans[2]['date'] == good_form_data['date2']
    assert vm.day_plans[2]['start'] == good_form_data['start2']
    assert vm.day_plans[2]['end'] == good_form_data['end2']
    assert vm.day_plans[2]['route'] == good_form_data['route2']
    assert vm.day_plans[2]['mode'] == good_form_data['mode2']

    assert vm.car_plate == good_form_data['carplate']
    assert vm.car_make == good_form_data['carmake']
    assert vm.car_model == good_form_data['carmodel']
    assert vm.car_color == good_form_data['carcolor']
    assert vm.car_location == good_form_data['carlocation']

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

    assert vm.days_of_food == good_form_data['daysoffood']
    assert vm.radio_monitor_time == good_form_data['radiomonitortime']
    # assert vm.off_trail_travel == good_form_data['offtrailtravel']
    assert vm.off_trail_travel is True
    # Need off trail travel map
    assert vm.cell_number == good_form_data['cellnumber']
    assert vm.satellite_number == good_form_data['satellitenumber']

    assert vm.contact_email0 == good_form_data['contactemail0']
    assert vm.contact_work0 == good_form_data['contactwork0']
    assert vm.contact_home0 == good_form_data['contacthome0']
    assert vm.contact_cell0 == good_form_data['contactcell0']
    assert vm.contact_email1 == good_form_data['contactemail1']
    assert vm.contact_work1 == good_form_data['contactwork1']
    assert vm.contact_home1 == good_form_data['contacthome1']
    assert vm.contact_cell1 == good_form_data['contactcell1']

    assert vm.s_avg == good_form_data['savg']
    assert vm.p_avg == good_form_data['pavg']
    assert vm.cr_avg == good_form_data['cravg']
    assert vm.c_avg == good_form_data['cavg']
    assert vm.ts_avg == good_form_data['tsavg']
    assert vm.tf_avg == good_form_data['tfavg']
    assert vm.e_avg == good_form_data['eavg']
    assert vm.ic_avg == good_form_data['icavg']

    assert vm.gar_avg == good_form_data['garavg']
    assert vm.mitigated_avg == good_form_data['mitigatedavg']
    assert vm.gar_mitigations == good_form_data['garmitigations']
    assert vm.notes == good_form_data['notes']
