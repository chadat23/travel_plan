import os
from typing import List

import folium
from flask import Blueprint

from travel_plan.infrastructure.view_modifiers import response
from travel_plan.viewmodels.map.all_locations_viewmodel import AllLocationsViewModel
from travel_plan.viewmodels.map.traveled_locations_viewmodel import TraveledLocationsViewModel

blueprint = Blueprint('map', __name__, template_folder='templates')

# https://leaflet-extras.github.io/leaflet-providers/preview/


@blueprint.route('/map/traveled-locations')
@response(template_file='map/full_page_map.html')
def traveled_locations():
    vm = TraveledLocationsViewModel()

    return vm.to_dict()


@blueprint.route('/map/all-locations')
@response(template_file='map/full_page_map.html')
def all_locations():
    vm = AllLocationsViewModel()

    return vm.to_dict()
