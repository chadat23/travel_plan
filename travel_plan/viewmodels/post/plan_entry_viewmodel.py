import datetime
from typing import List

import flask

from travel_plan.nosql_models.patroller import Patroller
from travel_plan.services import location_services, patroller_services
from travel_plan.viewmodels.shared.viewmodelbase import ViewModelBase


class PlanEntryViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()

        self.entry_date: str = self.request_dict.entrydate
        self.entry_location: str = self.request_dict.entrylocation
        self.exit_date: str = self.request_dict.exitdate
        self.exit_location: str = self.request_dict.exitlocation
        self.locations: List[str] = location_services.all_location_names()

        if self.request_dict.tracked == 'yes':
            self.tracked: str = 'checked'
            self.nottracked: str = ''
        else:
            self.tracked: str = ''
            self.nottracked: str = 'checked'

        self.plb: str = self.request_dict.plb

        self.users: List[Patroller] = patroller_services.all_patrollers()

        self.name0 = self.request_dict.name0
        self.call_sign0 = self.request_dict.callsign0
        self.pack_color0 = self.request_dict.packcolor0

        self.name1 = self.request_dict.name1
        self.call_sign1 = self.request_dict.callsign1
        self.pack_color1 = self.request_dict.packcolor1

        self.name2 = self.request_dict.name2
        self.call_sign2 = self.request_dict.callsign2
        self.pack_color2 = self.request_dict.packcolor2

        self.name2 = self.request_dict.name2
        self.call_sign2 = self.request_dict.callsign2
        self.pack_color2 = self.request_dict.packcolor2

        self.patrol_names = [['date0', 'start0', 'end0', 'route0', 'mode0'],
                             ['date1', 'start1', 'end1', 'route1', 'mode1']
                             ]
        self.patrol_values = [['', '', '', '', ''],
                              ['', '', '', '', ''],]
        self.date0 = self.request_dict.date0
