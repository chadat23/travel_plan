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

    target = 'travel_plan.infrastructure.file_util.save_files_with_name'
    saver = unittest.mock.patch(target, return_value=[])
    target = 'travel_plan.infrastructure.pdf_util.make_and_save_pdf'
    pdf_stuff = unittest.mock.patch(target, return_value=[])
    target = 'travel_plan.infrastructure.email_util.email_files'
    emailer = unittest.mock.patch(target, return_value=[])
    with flask_app.test_request_context(path='/travel/entry', data=form_data):
        with saver, pdf_stuff, emailer:
            resp: Response = entry_post()

    travel = travel_services.get_travel_by_id(1)

    assert travel.start_date == datetime.datetime.strptime(form_data['startdate'], '%Y-%m-%d').date()
    assert travel.entry_point.name == form_data['entrypoint']
    assert travel.end_date == datetime.datetime.strptime(form_data['enddate'], '%Y-%m-%d').date()
    assert travel.entry_point.name == form_data['exitpoint']
    assert travel.tracked
    assert travel.plb == form_data['plb']

    for i, t in enumerate(travel.travelers):
        assert t.traveler.name == form_data['travelername' + str(i)]
        assert t.call_sign == form_data['callsign' + str(i)]
        assert t.pack_color == form_data['packcolor' + str(i)]
        assert t.tent_color.lower() == form_data['tentcolor' + str(i)].lower()
        assert t.fly_color == form_data['flycolor' + str(i)]

    for i, d in enumerate(travel.travel_days):
        assert d.date == datetime.datetime.strptime(form_data['date' + str(i)], '%Y-%m-%d').date()
        assert d.starting_point.name == form_data['startingpoint' + str(i)]
        assert d.ending_point.name == form_data['endingpoint' + str(i)]
        assert d.route == form_data['route' + str(i)]
        assert d.mode == form_data['mode' + str(i)]
