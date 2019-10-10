from flask import Blueprint, current_app, jsonify, redirect, request, url_for

from travel_plan.infrastructure import file_util, pdf_util, email_util
from travel_plan.travel.travel_days import TravelDay
from travel_plan.travel.travel_file import TravelFile
from travel_plan.travel.travel_user_units import TravelUserUnit
from travel_plan.infrastructure.view_modifiers import response
from travel_plan.user.users import User
from travel_plan.travel import travel_services
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

    vm.convert_empty_strings_to_none()

    travel_user_units = [TravelUserUnit(**t) for t in vm.travelers if t['traveler_name']]

    day_plans = [TravelDay(**pd) for pd in vm.day_plans if pd['date']]

    emergency_contacts = [User(u['contact_name'], u['contact_email'], u['contact_work'],
                               u['contact_home'], u['contact_cell'], None, None) for u in vm.contacts]

    base_name = file_util.generate_name(vm.trip_leader_name, vm.start_date)

    travel_files = [TravelFile(f) for f in
                    file_util.save_files_with_name(vm.uploaded_files, base_name, current_app.config['PDF_FOLDER_PATH'])]
    travel_files.append(TravelFile(base_name + '.pdf'))

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
                                            vm.notes, travel_files
                                            )

    travel = travel_services.get_travel_from_id(travel_id)

    pdf_util.make_and_save_pdf(travel, base_name, current_app.config['PDF_FOLDER_PATH'])

    email_util.email_travel(travel, [f.name for f in travel_files], current_app.config['PDF_FOLDER_PATH'])

    return redirect(url_for('travel.email_sent'))


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


@blueprint.route('/travel/get-travelunit-info', methods=['GET'])
def get_responsible_party_info():
    print('starting')
    name = request.args.get('name', None, type=str)
    travelunit = travel_services.get_latest_travelunit_from_name(name)
    if travelunit.call_sign:
        call_sign = travelunit.call_sign
    else:
        call_sign = ''
    if travelunit.pack_color:
        pack_color = travelunit.pack_color.name
    else:
        pack_color = ''
    if travelunit.tent_color:
        tent_color = travelunit.tent_color.name
    else:
        tent_color = ''
    if travelunit.fly_color:
        fly_color = travelunit.fly_color.name
    else:
        fly_color = ''
    print('stuff', call_sign, pack_color, tent_color, fly_color)
    return jsonify(call_sign=call_sign, pack_color=pack_color, tent_color=tent_color, fly_color=fly_color)
