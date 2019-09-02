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

    vm.validate()

    assert vm.entry_date == good_form_data['entrydate']
    assert vm.entry_point == good_form_data['entrypoint']
    assert vm.exit_date == good_form_data['exitdate']
    assert vm.exit_point == good_form_data['exitpoint']
