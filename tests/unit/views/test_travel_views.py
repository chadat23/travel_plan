from flask import Response
from werkzeug.wrappers.response import Response as werkzeug_response

from tests.test_client import flask_app

import unittest.mock


def test_travel_view_entry_post_success(db_session_w_info, form_data,
                                        initialized_users, initialized_locations, initialized_cars,
                                        initialized_colors):
    from travel_plan.views.travel_views import entry_post
    from unittest.mock import Mock

    request = flask_app.test_request_context(path='/travel/entry', data=form_data)
    target = 'travel_plan.infrastructure.file_util.generate_name'
    namer = unittest.mock.patch(target, return_value='name')
    target = 'travel_plan.infrastructure.file_util.save_files_with_name'
    saver = unittest.mock.patch(target, return_value=[])
    target = 'travel_plan.infrastructure.pdf_util.make_and_save_pdf'
    pdf_stuff = unittest.mock.patch(target, return_value=[])
    target = 'travel_plan.infrastructure.email_util.email_files'
    emailer = unittest.mock.patch(target, return_value=[])
    target = 'travel_plan.services.travel_services.get_travel_by_id'
    get_travel = unittest.mock.patch(target, return_value=None)
    target = 'travel_plan.services.travel_services.create_plan'
    with unittest.mock.patch(target, retun_value=1) as plan:
        with namer, saver, pdf_stuff, emailer, get_travel, request:
            resp: Response = entry_post()

    assert isinstance(resp, Response) or isinstance(resp, werkzeug_response)
    plan.assert_called()


def test_travel_view_entry_post_fails_validation(db_session_w_info, form_data,
                                                 initialized_users, initialized_locations, initialized_cars,
                                                 initialized_colors):
    from datetime import datetime, timedelta
    from unittest.mock import Mock

    from travel_plan.views.travel_views import entry_post

    start_date = datetime.strptime(form_data['startdate'], '%Y-%m-%d')
    start_date = start_date - timedelta(days=5)
    start_date = datetime.strftime(start_date, '%Y-%m-%d')
    form_data['enddate'] = start_date
    form_data['date2'] = start_date

    request = flask_app.test_request_context(path='/travel/entry', data=form_data)
    target = 'travel_plan.services.travel_services.create_plan'
    with unittest.mock.patch(target, retun_value=None) as plan:
        with request:
            resp: Response = entry_post()

    assert isinstance(resp, Response)
    plan.assert_not_called()
