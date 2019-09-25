from typing import List

import folium

from travel_plan.travel import travel_services
from travel_plan.location.locations import Location
from travel_plan.viewmodels.shared.viewmodelbase import ViewModelBase
from travel_plan.map import map_utils


class TraveledLocationsViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()

        park_map = map_utils.get_map(map_utils.park_center)
        locations: List[Location] = travel_services.get_lat_long_frequencies()

        for loc, freq in locations.items():
            folium.CircleMarker(
                location=loc,
                radius=freq * 5,
                color='#428bca',
                fill=True,
                fill_color='#428bca'
            ).add_to(park_map)

        html = map_utils.parse_map_html(park_map)

        self.head: str = html.head
        self.body: str = html.body
        self.scripts: str = html.scripts

        self.title = 'All Locations'
