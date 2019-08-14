import os
from typing import List

import folium
from flask import Blueprint

from travel_plan.infrastructure.view_modifiers import response
from travel_plan.viewmodels.map.all_locations_viewmodel import AllLocationsViewModel
from travel_plan.viewmodels.map.patrolled_locations_viewmodel import PatrolledLocationsViewModel

blueprint = Blueprint('map', __name__, template_folder='templates')

# https://leaflet-extras.github.io/leaflet-providers/preview/


@blueprint.route('/map/patrolled-locations')
@response(template_file='map/full_page_map.html')
def patrolled_locations():
    vm = PatrolledLocationsViewModel()

    return vm.to_dict()


@blueprint.route('/map/all-locations')
@response(template_file='map/full_page_map.html')
def all_locations():
    vm = AllLocationsViewModel()

    return vm.to_dict()
