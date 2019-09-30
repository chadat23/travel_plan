from typing import List

from travel_plan.location import location_services, proposed_location_services
from travel_plan.location.locations import Location
from travel_plan.location.proposed_locations import StatusEnum
from travel_plan.viewmodels.shared.viewmodelbase import ViewModelBase
from travel_plan.map import map_utils


class ProposeLocationViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()

        self.name: str = self.request_dict.name
        self.latitude: str = self.request_dict.latitude
        self.longitude: str = self.request_dict.longitude
        self.note: str = self.request_dict.note

        park_map = map_utils.get_map(map_utils.park_center)

        locations: List[Location] = location_services.get_all()
        park_map = map_utils.add_locations_to_map(park_map, locations,
                                                  lambda loc: f'<strong>{loc.latitude}, {loc.longitude}<strong>',
                                                  lambda loc: f'Existing: {loc.name}')

        for location in proposed_location_services.all_locations():
            if location.status == StatusEnum.pending:
                park_map = map_utils.add_location_to_map(park_map, location,
                                                         lambda loc: f'<strong>{loc.latitude}, {loc.longitude}<strong>',
                                                         lambda loc: f'Pending: {loc.name}',
                                                         color='orange')
            else:
                park_map = map_utils.add_location_to_map(park_map, location,
                                                         lambda loc: f'<strong>{loc.latitude}, {loc.longitude}<strong>',
                                                         lambda loc: f'Rejected: {loc.name}',
                                                         color='red')

        html = map_utils.parse_map_html(park_map)

        # self.head: str = html.head + """ <script src="{{ url_for('static', filename='css/map.css') }}"></script>"""
        self.head: str = html.head
        self.body: str = html.body
        self.scripts: str = html.scripts

        self.title = 'Propose Location'
