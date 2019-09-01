from flask import Response

from tests.test_client import flask_app, client
from travel_plan.viewmodels.travel.travel_entry_viewmodel import TravelEntryViewModel

import unittest.mock


def test_travel_entry_vm_success():
    form_data = {
        'entrydate': '2019-6-18', 'entrypoint': 'May Lake TH',
    }

    with flask_app.test_request_context(path='/travel/entey', data=form_data):
        vm = TravelEntryViewModel()

    assert vm.entry_date == form_data['entrydate']
