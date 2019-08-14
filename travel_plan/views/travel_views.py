from flask import Blueprint, redirect, url_for

from travel_plan.disseminate import emailer
from travel_plan.infrastructure.view_modifiers import response
from travel_plan.services import travel_services
from travel_plan.viewmodels.travel.travel_entry_viewmodel import TravelEntryViewModel

blueprint = Blueprint('travel', __name__, template_folder='templates')


@blueprint.route('/travel/entry', methods=['GET'])
@response(template_file='travel/entry.html')
def entry_get():
    vm = TravelEntryViewModel()

    return vm.to_dict()


@blueprint.route('/travel/entry', methods=['POST'])
# @response(template_file='travel/entry.html')
def entry_post():
    vm = TravelEntryViewModel()

    entry = travel_services.create_plan(vm.entry_date, vm.entry_point, vm.exit_date, vm.exit_point,
                                        vm.tracked, vm.plb,
                                        vm.name0, vm.call_sign0, vm.pack_color0,
                                        vm.name1, vm.call_sign1, vm.pack_color1,
                                        vm.name2, vm.call_sign2, vm.pack_color2,
                                        vm.name3, vm.call_sign3, vm.pack_color3,
                                        vm.date0, vm.start0, vm.end0, vm.route0, vm.mode0,
                                        vm.date1, vm.start1, vm.end1, vm.route1, vm.mode1,
                                        vm.date2, vm.start2, vm.end2, vm.route2, vm.mode2,
                                        vm.contact0, vm.contact1
                                        )

    emailer.email_pdf(vm.entry_date, vm.entry_point, vm.exit_date, vm.exit_point,
                      vm.tracked, vm.plb,
                      vm.name0, vm.call_sign0, vm.pack_color0,
                      vm.name1, vm.call_sign1, vm.pack_color1,
                      vm.name2, vm.call_sign2, vm.pack_color2,
                      vm.name3, vm.call_sign3, vm.pack_color3,
                      vm.date0, vm.start0, vm.end0, vm.route0, vm.mode0,
                      vm.date1, vm.start1, vm.end1, vm.route1, vm.mode1,
                      vm.date2, vm.start2, vm.end2, vm.route2, vm.mode2,
                      vm.contact0, vm.contact1
                      )

    # return vm.to_dict()
    return redirect(url_for('travel.email_sent'))


@blueprint.route('/travel/sent', methods=['GET'])
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
