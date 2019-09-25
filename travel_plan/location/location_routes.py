from flask import Blueprint, url_for, redirect

from travel_plan.infrastructure.view_modifiers import response
from travel_plan.location import location_services, proposed_location_services
from travel_plan.viewmodels.location.assess_locations_viewmodel import AssessLocationsViewModel
from travel_plan.viewmodels.location.propose_location_viewmodel import ProposeLocationViewModel

blueprint = Blueprint('location', __name__, template_folder='templates')


@blueprint.route('/location/propose-location', methods=['GET'])
@response(template_file='location/propose_location.html')
def propose_location_get():
    vm = ProposeLocationViewModel()

    return vm.to_dict()


@blueprint.route('/location/propose-location', methods=['POST'])
@response(template_file='location/propose_location.html')
def propose_location_post():
    vm = ProposeLocationViewModel()
    # vm.validate()

    if vm.name.lower().strip() in [name.strip().lower() for name in location_services.all_location_names()]:
        vm.error = "This location name is already used."
        return vm.to_dict()
    else:
        if proposed_location_services.submit_location(vm.name, vm.latitude, vm.longitude, vm.note):
            return redirect(url_for('location.location_submitted'))
        else:
            vm.error = "There was a problem. Maybe try again?"
            return vm.to_dict()


@blueprint.route('/location/location-submitted')
@response(template_file='location/location_submitted.html')
def location_submitted():
    return {}


@blueprint.route('/location/assess-locations', methods=['GET'])
@response(template_file='map/full_page_map.html')
def assess_locations_get():
    vm = AssessLocationsViewModel()

    return vm.to_dict()


# @blueprint.route('/location/assess-locations/<location_name>/<accept_reject>', methods=['POST'])
# @blueprint.route('/location/assess-locations/<location_name>/<accept_reject>')
@blueprint.route('/location/assess-locations', methods=['POST'])
@response(template_file='map/full_page_map.html')
# def assess_locations_post(location_name: str, accept_reject: str):
def assess_locations_post():
    vm = AssessLocationsViewModel()
    # vm.validate()

    if ':approved' in vm.location_result:
        approved = True
        location_name = vm.location_result[:-9]
    else:
        approved = False
        location_name = vm.location_result[:-9]

    if vm.name.lower().strip() in [name.strip().lower() for name in location_services.all_location_names()]:
        vm.error = "This location name is already used."
        return vm.to_dict()
    else:
        if proposed_location_services.submit_location(vm.name, vm.latitude, vm.longitude, vm.note):
            return redirect(url_for('location.location_submitted'))
        else:
            vm.error = "There was a problem. Maybe try again?"
            return vm.to_dict()
