from flask import Blueprint, redirect

from travel_plan.config import PDF_FOLDER_PATH
from travel_plan.infrastructure import file_util, pdf_util, email_util
from travel_plan.infrastructure.view_modifiers import response
from travel_plan.models.travel_user_units import TravelUserUnit
from travel_plan.models.travel_days import TravelDay
from travel_plan.models.users import User
from travel_plan.services import travel_services
from travel_plan.viewmodels.travel.travel_entry_viewmodel import TravelEntryViewModel

blueprint = Blueprint('travel', __name__, template_folder='templates')


@blueprint.route('/travel/entry', methods=['GET'])
@response(template_file='travel/entry.html')
def entry_get():
    vm = TravelEntryViewModel()

    return vm.to_dict()


@blueprint.route('/travel/entry', methods=['POST'])
@response(template_file='travel/entry.html')
def entry_post():
    vm = TravelEntryViewModel()
    vm.validate()
    if vm.error:
        return vm.to_dict()

    travel_user_units = [TravelUserUnit(**t) for t in vm.travelers if t['traveler_name']]

    day_plans = [TravelDay(**pd) for pd in vm.day_plans if pd['date']]

    emergency_contacts = [User(u['contact_email'].split('@')[0], u['contact_email'], u['contact_work'],
                               u['contact_home'], u['contact_cell']) for u in vm.contacts]

    travel_id = travel_services.create_plan(vm.start_date, vm.entry_point, vm.end_date, vm.exit_point, vm.tracked,
                                            vm.plb,
                                            vm.trip_leader_name,
                                            travel_user_units, day_plans,
                                            vm.car_plate, vm.car_make, vm.car_model, vm.car_color, vm.car_location,
                                            vm.bivy_gear,
                                            vm.compass,
                                            vm.first_aid_kit,
                                            vm.flagging,
                                            vm.flare,
                                            vm.flashlight,
                                            vm.gps,
                                            vm.head_lamp,
                                            vm.helmet,
                                            vm.ice_axe,
                                            vm.map,
                                            vm.matches,
                                            vm.probe_pole,
                                            vm.radio,
                                            vm.rope,
                                            vm.shovel,
                                            vm.signal_mirror,
                                            vm.space_blanket,
                                            vm.spare_battery,
                                            vm.tent,
                                            vm.whistle,
                                            vm.days_of_food, vm.weapon, vm.radio_monitor_time, vm.off_trail_travel,
                                            vm.cell_number, vm.satellite_number, emergency_contacts,
                                            vm.gar_avg, vm.mitigated_gar, vm.gar_mitigations,
                                            vm.notes
                                            )

    travel = travel_services.get_travel_by_id(travel_id)

    base_name = file_util.generate_name(travel)

    files = file_util.save_files_with_name(vm.uploaded_files, base_name, PDF_FOLDER_PATH)

    files.append(pdf_util.make_and_save_pdf(travel, base_name, PDF_FOLDER_PATH))

    email_util.email_files(travel, files)

    # return redirect(url_for('travel.email_sent'))
    return redirect('/travel/email-sent')


@blueprint.route('/travel/email-sent')
@response(template_file='travel/sent.html')
def email_sent():
    return {}


@blueprint.route('/travel/add-traveler')
@response(template_file='travel/entry.html')
def add_traveler():
    vm = TravelEntryViewModel()

    return vm.to_dict()


@blueprint.route('/travel/search', methods=['GET'])
@response(template_file='travel/search.html')
def search():
    return {}
