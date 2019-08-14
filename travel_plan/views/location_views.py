import flask
from flask import Blueprint, url_for, redirect

from travel_plan.infrastructure.view_modifiers import response
from travel_plan.services import location_services
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
        pass

    return flask.redirect('/location/location-submitted')
    # return redirect(url_for('location.location_submitted'))
    # return redirect('/location/location-submitted')
    # return


@blueprint.route('/location/location-submitted')
@response(template_file='location/location_submitted.html')
def location_submitted():
    return {}
