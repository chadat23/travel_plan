import datetime
import unittest.mock

from flask import Response

from travel_plan.travel import travel_services


def test_get_travel_by_id(app_w_db, form_data):
    from travel_plan.travel.travel_routes import entry_post

    target = 'travel_plan.infrastructure.file_util.save_files_with_name'
    saver = unittest.mock.patch(target, return_value=[])
    target = 'travel_plan.infrastructure.pdf_util.make_and_save_pdf'
    pdf_stuff = unittest.mock.patch(target, return_value=[])
    target = 'travel_plan.infrastructure.email_util.email_travel'
    emailer = unittest.mock.patch(target, return_value=[])
    target = 'travel_plan.services.color_services.get_id_by_name'
    test_color = unittest.mock.patch(target, return_value=3)
    with app_w_db.test_request_context(path='/travel/entry', data=form_data):
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
        assert t.pack_color.name == form_data['packcolor' + str(i)]
        assert t.tent_color.name == form_data['tentcolor' + str(i)].lower().title()
        assert t.fly_color.name == form_data['flycolor' + str(i)]

    for i, d in enumerate(travel.travel_days):
        assert d.date == datetime.datetime.strptime(form_data['date' + str(i)], '%Y-%m-%d').date()
        assert d.starting_point.name == form_data['startingpoint' + str(i)]
        assert d.ending_point.name == form_data['endingpoint' + str(i)]
        assert d.route == form_data['route' + str(i)]
        assert d.mode == form_data['mode' + str(i)]

    for i, c in enumerate(travel.contacts):
        assert c.name == form_data['contactname' + str(i)]
        assert c.email == form_data['contactemail' + str(i)]
        assert c.home_number == form_data['contacthome' + str(i)]


def test_get_travel_by_id_w_nones(app_w_db, form_data_w_nones):
    from travel_plan.travel.travel_routes import entry_post

    target = 'travel_plan.infrastructure.file_util.save_files_with_name'
    saver = unittest.mock.patch(target, return_value=[])
    target = 'travel_plan.infrastructure.pdf_util.make_and_save_pdf'
    pdf_stuff = unittest.mock.patch(target, return_value=[])
    target = 'travel_plan.infrastructure.email_util.email_travel'
    emailer = unittest.mock.patch(target, return_value=[])
    target = 'travel_plan.services.color_services.get_id_by_name'
    test_color = unittest.mock.patch(target, return_value=3)
    with app_w_db.test_request_context(path='/travel/entry', data=form_data_w_nones):
        with saver, pdf_stuff, emailer:
            resp: Response = entry_post()

    travel = travel_services.get_travel_by_id(1)

    assert travel.start_date == datetime.datetime.strptime(form_data_w_nones['startdate'], '%Y-%m-%d').date()
    assert travel.entry_point.name == form_data_w_nones['entrypoint']
    assert travel.end_date == datetime.datetime.strptime(form_data_w_nones['enddate'], '%Y-%m-%d').date()
    assert travel.entry_point.name == form_data_w_nones['exitpoint']
    assert travel.tracked
    assert travel.plb == None

    for i, t in enumerate(travel.travelers):
        assert t.traveler.name == form_data_w_nones['travelername' + str(i)]
        assert t.call_sign == form_data_w_nones['callsign' + str(i)]
        assert t.pack_color == None
        assert t.tent_color == None
        assert t.fly_color == None

    for i, d in enumerate(travel.travel_days):
        assert d.date == datetime.datetime.strptime(form_data_w_nones['date' + str(i)], '%Y-%m-%d').date()
        assert d.starting_point.name == form_data_w_nones['startingpoint' + str(i)]
        assert d.ending_point.name == form_data_w_nones['endingpoint' + str(i)]
        assert d.route == form_data_w_nones['route' + str(i)]
        assert d.mode == form_data_w_nones['mode' + str(i)]

    for i, c in enumerate(travel.contacts):
        assert c.name == form_data_w_nones['contactname' + str(i)]
