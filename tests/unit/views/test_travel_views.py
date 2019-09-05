from flask import Response

from tests.test_client import flask_app

import unittest.mock


def test_travel_view_entry_post_success(form_data, initialized_users, initialized_locations, initialized_cars,
                                        initialized_colors):
    from travel_plan.views.travel_views import entry_post
    from unittest.mock import Mock

    m = Mock()
    m.side_effect = initialized_users[:2]
    target = 'travel_plan.services.user_services.get_user_from_name'
    user_names = unittest.mock.patch(target, return_value=m())
    m.side_effect = [1, 2]
    target = 'travel_plan.services.location_services.get_id_from_name'
    location_ids = unittest.mock.patch(target, return_value=m())

    target = 'travel_plan.services.color_services.add_if_not_present'
    test_color = unittest.mock.patch(target, return_value='Red')

    target = 'travel_plan.services.location_services.get_names'
    get_location_names = unittest.mock.patch(target, return_value=[a.name for a in initialized_locations])
    target = 'travel_plan.services.user_services.get_users'
    get_users = unittest.mock.patch(target, return_value=initialized_users)
    target = 'travel_plan.services.color_services.get_names'
    get_color_names = unittest.mock.patch(target, return_value=[c.id for c in initialized_colors])
    target = 'travel_plan.services.car_services.get_names'
    get_car_names = unittest.mock.patch(target, return_value=[c.plate for c in initialized_cars])

    request = flask_app.test_request_context(path='/travel/entry', data=form_data)

    with user_names, location_ids, test_color, get_location_names, get_users, get_color_names, get_car_names, request:
        resp: Response = entry_post()

    a = 0

    assert False
