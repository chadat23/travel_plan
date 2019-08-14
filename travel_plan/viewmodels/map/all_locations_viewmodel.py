from typing import List

import folium

from travel_plan.services import location_services
from travel_plan.sql_models.locations import Location
from travel_plan.viewmodels.shared.viewmodelbase import ViewModelBase
from travel_plan.views import _util


class AllLocationsViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()

        locations: List[Location] = location_services.all_locations()

        park_map = _util.get_map(_util.park_center)

        for loc in locations:
            folium.Marker(
                location=[loc.latitude, loc.longitude],
                popup=f'<strong>{loc.latitude}, {loc.longitude}<strong>',  # popup can have html
                tooltip=loc.name,
            ).add_to(park_map)

        html = _util.parse_map_html(park_map)

        self.head: str = html.head
        self.body: str = html.body
        self.scripts: str = html.scripts

        self.title = 'All Locations'
