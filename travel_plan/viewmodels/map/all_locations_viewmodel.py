from typing import List

import folium

from travel_plan.services import location_services
from travel_plan.sql_models.locations import Location
from travel_plan.viewmodels.shared.viewmodelbase import ViewModelBase
from travel_plan.views import view_utils


class AllLocationsViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()

        park_map = view_utils.get_map(view_utils.park_center)
        locations: List[Location] = location_services.all_locations()
        park_map = view_utils.add_locations_to_map(park_map, locations,
                                                   lambda loc: f'<strong>{loc.latitude}, {loc.longitude}<strong>',
                                                   lambda loc: f'{loc.name}')

        html = view_utils.parse_map_html(park_map)

        self.head: str = html.head
        self.body: str = html.body
        self.scripts: str = html.scripts

        self.title = 'All Locations'
