from typing import List

import flask

from travel_plan.services import location_services, user_services, car_services, color_services
from travel_plan.models.users import User
from travel_plan.viewmodels.shared.viewmodelbase import ViewModelBase


class TravelEntryViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()

        self.entry_date: str = self.request_dict.entrydate
        self.entry_point: str = self.request_dict.entrypoint
        self.exit_date: str = self.request_dict.exitdate
        self.exit_point: str = self.request_dict.exitpoint
        self.locations: List[str] = location_services.get_names()

        if self.request_dict.tracked == '':
            self.tracked = 'yes'
        else:
            self.tracked = self.request_dict.tracked == 'yes'

        self.plb: str = self.request_dict.plb

        self.users: List[User] = user_services.get_users()
        self.colors: List[str] = color_services.get_names()

        request = flask.request
        self.patrollers = []
        # i = 0
        # while 'name' + str(i) in request.form:
        #     p = {}
        #     p['name'] = request.form['name' + str(i)]
        #     p['call_sign'] = request.form['call_sign' + str(i)]
        #     p['pack_color'] = request.form['pack_color' + str(i)]
        #     i += 1
        for i in range(4):
            p = {}
            if 'name' + str(i) in request.form:
                p['name'] = request.form['name' + str(i)]
                p['call_sign'] = request.form['callsign' + str(i)]
                p['pack_color'] = request.form['packcolor' + str(i)]
                p['tent_color'] = request.form['tentcolor' + str(i)]
                p['fly_color'] = request.form['flycolor' + str(i)]
            else:
                p['name'] = ''
                p['call_sign'] = ''
                p['pack_color'] = ''
                p['tent_color'] = ''
                p['fly_color'] = ''
            self.patrollers.append(p)

        self.day_plans = []
        for i in range(9):
            d_p = {}
            if 'date' + str(i) in request.form:
                d_p['date'] = request.form['date' + str(i)]
                d_p['start'] = request.form['start' + str(i)]
                d_p['end'] = request.form['end' + str(i)]
                d_p['route'] = request.form['route' + str(i)]
                d_p['mode'] = request.form['mode' + str(i)]
            else:
                d_p['date'] = ''
                d_p['start'] = ''
                d_p['end'] = ''
                d_p['route'] = ''
                d_p['mode'] = ''
            self.day_plans.append(d_p)

        self.cars = car_services.get_names()
        self.car_plate = self.request_dict.carmake
        self.car_make = self.request_dict.carmake
        self.car_model = self.request_dict.carmodel
        self.car_color = self.request_dict.carcolor

        self.bivy_gear = self.request_dict.bivygear
        self.compass = self.request_dict.compass
        self.first_aid_kit = self.request_dict.firstaidkit
        self.flagging = self.request_dict.flagging
        self.flare = self.request_dict.flare
        self.flashlight = self.request_dict.flashlight
        self.gps = self.request_dict.gps
        self.head_lamp = self.request_dict.headlamp
        self.helmet = self.request_dict.helmet
        self.ice_axe = self.request_dict.iceaxe
        self.map = self.request_dict.map
        self.matches = self.request_dict.matches
        self.pole_probe = self.request_dict.poleprobe
        self.radio = self.request_dict.radio
        self.rope = self.request_dict.rope
        self.shovel = self.request_dict.shovel
        self.signal_mirror = self.request_dict.signalmirror
        self.space_blanket = self.request_dict.spaceblanket
        self.spare_battery = self.request_dict.sparebattery
        self.tent = self.request_dict.tent
        self.whistle = self.request_dict.whistle

        self.days_of_food = self.request_dict.daysoffood
        self.weapon = self.request_dict.weapon
        self.radio_monitor_time = self.request_dict.radiomonitortime
        self.off_trail_travel = self.request_dict.offtrailtravel == 'yes'
        # https://www.tutorialspoint.com/flask/flask_file_uploading.htm
        # https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
        # self.off_trail_travel_map_file = self.request_dict.offtrailtravelmapfile
        if 'offtrailtravelmapfile' in request.files:
            # self.off_trail_travel_map_file = request.files['offtrailtravelmapfile']
            self.off_trail_travel_map_file = self.request_dict.offtrailtravelmapfile
        else:
            self.off_trail_travel_map_file = ''
        self.cell_number = self.request_dict.cellnumber
        self.satellite_number = self.request_dict.satellitenumber

        self.contact_email0 = self.request_dict.contactemail0
        self.contact_email1 = self.request_dict.contactemail1

        self.gars = []
        for i in range(4):
            gar = {}
            if 's' + str(i) in request.form:
                gar['s'] = request.form['s' + str(i)]
                gar['p'] = request.form['p' + str(i)]
                gar['cr'] = request.form['cr' + str(i)]
                gar['c'] = request.form['c' + str(i)]
                gar['ts'] = request.form['ts' + str(i)]
                gar['tf'] = request.form['tf' + str(i)]
                gar['e'] = request.form['e' + str(i)]
                gar['ic'] = request.form['ic' + str(i)]
            else:
                gar['s'] = ''
                gar['p'] = ''
                gar['cr'] = ''
                gar['c'] = ''
                gar['ts'] = ''
                gar['tf'] = ''
                gar['e'] = ''
                gar['ic'] = ''
            self.gars.append(gar)

    def validate(self):
        self._validate_dates()
        if self.error:
            return None

    def _validate_dates(self):
        if self.exit_date < self.entry_date:
            self.error = "Your exit date can't be before your entry date."

