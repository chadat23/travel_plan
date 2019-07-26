import flask

from travel_plan.infrastructure.view_modifiers import response
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

    return vm.to_dict()


@blueprint.route('/plans/add-patroller')
@response(template_file='plan/entry.html')
def add_patroler():
    vm = PlanEntryViewModel()

    return vm.to_dict()


@blueprint.route('/plans/search', methods=['GET'])
@response(template_file='plan/search.html')
def search():
    return {}
