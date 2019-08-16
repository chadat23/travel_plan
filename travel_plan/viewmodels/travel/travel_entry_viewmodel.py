from typing import List

from travel_plan.services import location_services, user_services
from travel_plan.sql_models.users import User
from travel_plan.viewmodels.shared.viewmodelbase import ViewModelBase


class TravelEntryViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()

        self.entry_date: str = self.request_dict.entrydate
        self.entry_point: str = self.request_dict.entrylocation
        self.exit_date: str = self.request_dict.exitdate
        self.exit_point: str = self.request_dict.exitlocation
        self.locations: List[str] = location_services.all_location_names()

        if self.request_dict.tracked == 'yes':
            self.tracked: str = 'checked'
            self.nottracked: str = ''
        else:
            self.tracked: str = ''
            self.nottracked: str = 'checked'

        self.plb: str = self.request_dict.plb

        self.users: List[User] = user_services.all_patrollers()

        self.name0 = self.request_dict.name0
        self.call_sign0 = self.request_dict.callsign0
        self.pack_color0 = self.request_dict.packcolor0

        self.name1 = self.request_dict.name1
        self.call_sign1 = self.request_dict.callsign1
        self.pack_color1 = self.request_dict.packcolor1

        self.name2 = self.request_dict.name2
        self.call_sign2 = self.request_dict.callsign2
        self.pack_color2 = self.request_dict.packcolor2

        self.name3 = self.request_dict.name3
        self.call_sign3 = self.request_dict.callsign3
        self.pack_color3 = self.request_dict.packcolor3

        self.date0 = self.request_dict.date0
        self.start0 = self.request_dict.start0
        self.end0 = self.request_dict.end0
        self.route0 = self.request_dict.route0
        self.mode0 = self.request_dict.mode0

        self.date1 = self.request_dict.date1
        self.start1 = self.request_dict.start1
        self.end1 = self.request_dict.end1
        self.route1 = self.request_dict.route1
        self.mode1 = self.request_dict.mode1

        self.date2 = self.request_dict.date2
        self.start2 = self.request_dict.start2
        self.end2 = self.request_dict.end2
        self.route2 = self.request_dict.route2
        self.mode2 = self.request_dict.mode2

        self.contact0 = self.request_dict.contact0
        self.contact1 = self.request_dict.contact1
