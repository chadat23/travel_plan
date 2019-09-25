from typing import List

from travel_plan.location import location_services, proposed_location_services
from travel_plan.location.locations import Location
from travel_plan.location.proposed_locations import StatusEnum
from travel_plan.viewmodels.shared.viewmodelbase import ViewModelBase
from travel_plan.map import map_utils as vutil


class AssessLocationsViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()

        self.location_result = self.request_dict.location_result

        park_map = vutil.get_map(vutil.park_center)

        locations: List[Location] = location_services.get_all()
        park_map = vutil.add_locations_to_map(park_map, locations,
                                              lambda loc: f'<strong>{loc.latitude}, {loc.longitude}<strong>',
                                              lambda loc: f'Existing: {loc.name}')

        for location in proposed_location_services.all_locations():
            if location.status == StatusEnum.pending:
                park_map = vutil.add_location_to_map(park_map, location,
                                                     lambda loc: f'<strong>{loc.latitude}, {loc.longitude}<strong> </br>'
                                                     + f'</br> {loc.note} </br>'
                                                     + '</br>'
                                                     + f'<button type="submit" class="btn btn-success" name="location_result" value="{loc.name}:approved">Approve</button>'
                                                     + '</br>'
                                                     + f'<button type="submit" class="btn btn-danger" name="location_result" value="{loc.name}:rejected">Reject</button>',
                                                     lambda loc: f'Pending: {loc.name}',
                                                     color='orange')
            else:
                park_map = vutil.add_location_to_map(park_map, location,
                                                     lambda
                                                         loc: f'<strong>{loc.latitude}, {loc.longitude}<strong>',
                                                     lambda loc: f'Rejected: {loc.name}',
                                                     color='red')

        html = vutil.parse_map_html(park_map)

        self.head: str = html.head
        # self.head: str = html.head + '<script src="' + url_for('static', filename='css/map.css') + '"></script>'
        self.body: str = '<form action="" method="POST" style="height: 700px;">' + html.body + '</form>'
        # self.body: str = '<form action="" method="POST">' + html.body + '</form>'
        # self.body: str = '<iframe height="200" width="300">' + html.body + '</iframe>'
        # self.body: str = '<form action="" method="POST">' + '</form>'  + html.body
        self.scripts: str = html.scripts

        self.title = 'Assess Locations'
