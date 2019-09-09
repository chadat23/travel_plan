from flask import Response
from werkzeug.wrappers.response import Response as werkzeug_response

from tests.test_client import flask_app

import unittest.mock


def test_(db_session_w_info, form_data, initialized_users, initialized_locations, initialized_cars,
          initialized_colors):
    from travel_plan.views.travel_views import entry_post

    with flask_app.test_request_context(path='/travel/entry', data=form_data):
        resp: Response = entry_post()

def test_travel_view_entry_post_success(db_session_w_info, form_data,
                                        initialized_users, initialized_locations, initialized_cars,
                                        initialized_colors):
    from travel_plan.views.travel_views import entry_post
    from unittest.mock import Mock

    request = flask_app.test_request_context(path='/travel/entry', data=form_data)
    target = 'travel_plan.disseminate.emailer.make_and_email_pdf'
    email_pdf = unittest.mock.patch(target, return_value=None)
    target = 'travel_plan.services.travel_services.create_plan'
    with unittest.mock.patch(target, retun_value=1) as plan:
        print(type(plan))
        with email_pdf, request:
            resp: Response = entry_post()

    assert isinstance(resp, Response) or isinstance(resp, werkzeug_response)
    plan.assert_called()


def test_travel_view_entry_post_fails_validation(db_session_w_info, form_data,
                                                 initialized_users, initialized_locations, initialized_cars,
                                                 initialized_colors):
    from datetime import datetime, timedelta
    from unittest.mock import Mock

    from travel_plan.views.travel_views import entry_post

    start_date = datetime.strptime(form_data['entrydate'], '%Y-%m-%d')
    start_date = start_date - timedelta(days=5)
    start_date = datetime.strftime(start_date, '%Y-%m-%d')
    form_data['exitdate'] = start_date
    form_data['date2'] = start_date

    request = flask_app.test_request_context(path='/travel/entry', data=form_data)
    target = 'travel_plan.disseminate.emailer.make_and_email_pdf'
    email_pdf = unittest.mock.patch(target, return_value=None)
    target = 'travel_plan.services.travel_services.create_plan'
    with unittest.mock.patch(target, retun_value=None) as plan:
        print(type(plan))
        with email_pdf, request:
            resp: Response = entry_post()

    assert isinstance(resp, Response)
    plan.assert_not_called()

# def test_junk_travel_view_entry_post_success(form_data, initialized_users, initialized_locations, initialized_cars,
#                                         initialized_colors):
#     from travel_plan.views.travel_views import entry_post
#     from unittest.mock import Mock

#     m = Mock()
#     m.side_effect = initialized_users[:2]
#     target = 'travel_plan.services.user_services.get_user_from_name'
#     user_names = unittest.mock.patch(target, return_value=m())
#     m.side_effect = [1, 2]
#     target = 'travel_plan.services.location_services.get_id_from_name'
#     location_ids = unittest.mock.patch(target, return_value=m())

#     target = 'travel_plan.services.color_services.add_if_not_present'
#     test_color = unittest.mock.patch(target, return_value='Red')

#     target = 'travel_plan.services.location_services.get_names'
#     get_location_names = unittest.mock.patch(target, return_value=[a.name for a in initialized_locations])
#     target = 'travel_plan.services.user_services.get_users'
#     get_users = unittest.mock.patch(target, return_value=initialized_users)
#     target = 'travel_plan.services.color_services.get_names'
#     get_color_names = unittest.mock.patch(target, return_value=[c.id for c in initialized_colors])
#     target = 'travel_plan.services.car_services.get_names'
#     get_car_names = unittest.mock.patch(target, return_value=[c.plate for c in initialized_cars])

#     request = flask_app.test_request_context(path='/travel/entry', data=form_data)

#     with user_names, location_ids, test_color, get_location_names, get_users, get_color_names, get_car_names, request:
#         resp: Response = entry_post()

#     a = 0

#     assert False
