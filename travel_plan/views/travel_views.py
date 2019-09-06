from flask import Blueprint, redirect, url_for

from travel_plan.disseminate import emailer
from travel_plan.infrastructure.view_modifiers import response
from travel_plan.models.patrol_user_units import PatrolUserUnit
from travel_plan.models.travel_days import PatrolDay
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

    patrol_user_units = [PatrolUserUnit(**p) for p in vm.patrollers if p['patroller_name']]

    day_plans = [PatrolDay(**pd) for pd in vm.day_plans if pd['date']]

    travel_services.create_plan(vm.entry_date, vm.entry_point, vm.exit_date, vm.exit_point,
                                vm.tracked, vm.plb,
                                patrol_user_units, day_plans,
                                vm.car_plate, vm.car_make, vm.car_model, vm.car_color, vm.car_location,
                                vm.bivy_gear == 'on',
                                vm.compass == 'on',
                                vm.first_aid_kit == 'on',
                                vm.flagging == 'on',
                                vm.flare == 'on',
                                vm.flashlight == 'on',
                                vm.gps == 'on',
                                vm.head_lamp == 'on',
                                vm.helmet == 'on',
                                vm.ice_axe == 'on',
                                vm.map == 'on',
                                vm.matches == 'on',
                                vm.probe_pole == 'on',
                                vm.radio == 'on',
                                vm.rope == 'on',
                                vm.shovel == 'on',
                                vm.signal_mirror == 'on',
                                vm.space_blanket == 'on',
                                vm.spare_battery == 'on',
                                vm.tent == 'on',
                                vm.whistle == 'on',
                                'a', 'b'
                                # vm.contact0, vm.contact1
                                )

    emailer.email_pdf(vm.entry_date, vm.entry_point, vm.exit_date, vm.exit_point,
                      vm.tracked, vm.plb,
                    #   vm.name0, vm.call_sign0, vm.pack_color0,
                    #   vm.name1, vm.call_sign1, vm.pack_color1,
                    #   vm.name2, vm.call_sign2, vm.pack_color2,
                    #   vm.name3, vm.call_sign3, vm.pack_color3,
                    #   vm.date0, vm.start0, vm.end0, vm.route0, vm.mode0,
                    #   vm.date1, vm.start1, vm.end1, vm.route1, vm.mode1,
                    #   vm.date2, vm.start2, vm.end2, vm.route2, vm.mode2,
                    #   vm.contact0, vm.contact1
                      )

    # return redirect(url_for('travel.email_sent'))
    return redirect('/travel/email-sent')


@blueprint.route('/travel/email-sent')
@response(template_file='travel/sent.html')
def email_sent():
    return {}


@blueprint.route('/travel/add-patroller')
@response(template_file='travel/entry.html')
def add_patroler():
    vm = TravelEntryViewModel()

    return vm.to_dict()


@blueprint.route('/travel/search', methods=['GET'])
@response(template_file='travel/search.html')
def search():
    return {}
