from flask import Response

from tests.test_client import flask_app


def test_123(db_session_w_info, form_data, initialized_users, initialized_locations, initialized_cars,
          initialized_colors):
    from travel_plan.views.travel_views import entry_post

    with flask_app.test_request_context(path='/travel/entry', data=form_data):
        resp: Response = entry_post()

    assert False
