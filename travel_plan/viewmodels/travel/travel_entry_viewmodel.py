from typing import List

import flask

from travel_plan.services import location_services, user_services
from travel_plan.models.users import User
from travel_plan.viewmodels.shared.viewmodelbase import ViewModelBase


class TravelEntryViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()

        self.entry_date: str = self.request_dict.entrydate
        self.entry_point: str = self.request_dict.entrylocation
        self.exit_date: str = self.request_dict.exitdate
        self.exit_point: str = self.request_dict.exitlocation
        self.locations: List[str] = location_services.get_names()

        if self.request_dict.tracked == 'yes':
            self.tracked: str = 'checked'
            self.nottracked: str = ''
        else:
            self.tracked: str = ''
            self.nottracked: str = 'checked'

        self.plb: str = self.request_dict.plb

        self.usernames: List[str] = user_services.get_names()

        self.leader_name = self.request_dict.leadername
        self.leader_call_sign = self.request_dict.leadercallsign
        self.leader_pack_color = self.request_dict.leaderpackcolor

        request = flask.request
        self.patrollers = []
        # i = 0
        # while 'name' + str(i) in request.form:
        #     p = {}
        #     p['name'] = request.form['name' + str(i)]
        #     p['call_sign'] = request.form['call_sign' + str(i)]
        #     p['pack_color'] = request.form['pack_color' + str(i)]
        #     i += 1
        for i in range(3):
            p = {}
            if 'name' + str(i) in request.form:
                p['name'] = request.form['name' + str(i)]
                p['callsign'] = request.form['callsign' + str(i)]
                p['packcolor'] = request.form['packcolor' + str(i)]
            else:
                p['name'] = ''
                p['callsign'] = ''
                p['packcolor'] = ''
            self.patrollers.append(p)

        self.days_plan = []
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
