from typing import Dict

import folium

from travel_plan.services import travel_services
from travel_plan.viewmodels.shared.viewmodelbase import ViewModelBase
from travel_plan.views import _util


class ProposeLocationViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()

        self.name: str = self.request_dict.name
        self.latitude: str = self.request_dict.latitude
        self.longitude: str = self.request_dict.longitude
        self.note: str = self.request_dict.note

        park_map = _util.get_map(_util.park_center)

        locations: Dict[tuple, int] = travel_services.get_lat_long_frequencies()

        for loc, freq in locations.items():
            folium.CircleMarker(
                location=loc,
                radius=freq * 5,
                color='#428bca',
                fill=True,
                fill_color='#428bca',
            ).add_to(park_map)

        html = _util.parse_map_html(park_map)

        self.head: str = html.head
        self.body: str = html.body
        self.scripts: str = html.scripts

        self.title = 'Propose Location'
