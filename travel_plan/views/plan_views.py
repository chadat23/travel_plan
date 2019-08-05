import flask

from travel_plan.disseminate import emailer
from travel_plan.infrastructure.view_modifiers import response
from travel_plan.services import patrol_services
from travel_plan.viewmodels.post.plan_entry_viewmodel import PlanEntryViewModel

blueprint = flask.Blueprint('plan', __name__, template_folder='templates')


@blueprint.route('/plans/entry', methods=['GET'])
@response(template_file='plan/entry.html')
def entry_get():
    vm = PlanEntryViewModel()

    return vm.to_dict()


@blueprint.route('/plans/entry', methods=['POST'])
@response(template_file='plan/entry.html')
def entry_post():
    vm = PlanEntryViewModel()

    entry = patrol_services.create_plan(vm.entry_date, vm.entry_point, vm.exit_date, vm.exit_point,
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

    return vm.to_dict()
    # return flask.redirect('/plans/sent')


@blueprint.route('/plans/sent')
@response(template_file='plan/sent.html')
def email_sent():
    return dict()


@blueprint.route('/plans/add-patroller')
@response(template_file='plan/entry.html')
def add_patroler():
    vm = PlanEntryViewModel()

    return vm.to_dict()


@blueprint.route('/plans/search', methods=['GET'])
@response(template_file='plan/search.html')
def search():
    return dict()
