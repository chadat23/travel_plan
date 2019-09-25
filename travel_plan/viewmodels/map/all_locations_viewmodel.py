from typing import List

from travel_plan.location import location_services
from travel_plan.location.locations import Location
from travel_plan.viewmodels.shared.viewmodelbase import ViewModelBase
from travel_plan.map import map_utils


class AllLocationsViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()

        park_map = map_utils.get_map(map_utils.park_center)
        locations: List[Location] = location_services.get_all()
        park_map = map_utils.add_locations_to_map(park_map, locations,
                                                  lambda loc: f'<strong>{loc.latitude}, {loc.longitude}<strong>',
                                                  lambda loc: f'{loc.name}')

        html = map_utils.parse_map_html(park_map)

        self.head: str = html.head
        self.body: str = html.body
        self.scripts: str = html.scripts

        self.title = 'All Locations'
