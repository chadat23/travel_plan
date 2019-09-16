import datetime
import unittest.mock

from flask import Response

from tests.test_client import flask_app
from travel_plan.services import travel_services


def ntest_123(db_session_w_info, form_data, initialized_users, initialized_locations, initialized_cars,
              initialized_colors):
    from travel_plan.views.travel_views import entry_post

    with flask_app.test_request_context(path='/travel/entry', data=form_data):
        resp: Response = entry_post()

    assert False


def test_get_travel_by_id(db_session_w_info, form_data, initialized_users, initialized_locations, initialized_cars,
                          initialized_colors):
    from travel_plan.views.travel_views import entry_post

    target = 'travel_plan.disseminate.emailer.make_and_email_pdf'
    emailer = unittest.mock.patch(target, return_value=None)
    with flask_app.test_request_context(path='/travel/entry', data=form_data):
        with emailer:
            resp: Response = entry_post()

    travel = travel_services.get_travel_by_id(1)

    assert travel.start_date == datetime.datetime.strptime(form_data['startdate'], '%Y-%m-%d').date()
