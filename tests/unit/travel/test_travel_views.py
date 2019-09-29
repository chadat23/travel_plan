from flask import Response
from werkzeug.wrappers.response import Response as werkzeug_response

import unittest.mock

from travel_plan.travel.travels import Travel


def test_travel_view_entry_post_success(app_w_db, form_data):
    from travel_plan.travel.travel_routes import entry_post
    from unittest.mock import Mock

    request = app_w_db.test_request_context(path='/travel/entry', data=form_data)
    target = 'travel_plan.infrastructure.file_util.generate_name'
    namer = unittest.mock.patch(target, return_value='name')
    target = 'travel_plan.infrastructure.file_util.save_files_with_name'
    saver = unittest.mock.patch(target, return_value=[])
    target = 'travel_plan.infrastructure.pdf_util.make_and_save_pdf'
    pdf_stuff = unittest.mock.patch(target, return_value=[])
    target = 'travel_plan.infrastructure.email_util.email_travel'
    emailer = unittest.mock.patch(target, return_value=[])
    target = 'travel_plan.travel.travel_services.get_travel_by_id'
    get_travel = unittest.mock.patch(target, return_value=Travel(*range(40)))
    target = 'travel_plan.travel.travels.Travel.get_contact_list'
    get_contacts = unittest.mock.patch(target, return_value=[])
    target1 = 'travel_plan.travel.travel_services.create_plan'
    target2 = 'travel_plan.travel.travels.Travel'
    with unittest.mock.patch(target1, return_value=1) as create_plan:
        with namer, saver, pdf_stuff, emailer, get_travel, request, get_contacts:
            resp: Response = entry_post()

    assert isinstance(resp, Response) or isinstance(resp, werkzeug_response)
    create_plan.assert_called()


def test_travel_view_entry_post_fails_validation(app_w_db, form_data):
    from datetime import datetime, timedelta
    from unittest.mock import Mock

    from travel_plan.travel.travel_routes import entry_post

    start_date = datetime.strptime(form_data['startdate'], '%Y-%m-%d')
    start_date = start_date - timedelta(days=5)
    start_date = datetime.strftime(start_date, '%Y-%m-%d')
    form_data['enddate'] = start_date
    form_data['date2'] = start_date

    request = app_w_db.test_request_context(path='/travel/entry', data=form_data)
    target = 'travel_plan.travel.travel_services.create_plan'
    with unittest.mock.patch(target, retun_value=None) as plan:
        with request:
            resp: Response = entry_post()

    assert isinstance(resp, Response)
    plan.assert_not_called()
