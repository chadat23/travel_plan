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
        # while 'patroller_name' + str(i) in request.form:
        #     p = {}
        #     p['patroller_name'] = request.form['patroller_name' + str(i)]
        #     p['call_sign'] = request.form['call_sign' + str(i)]
        #     p['pack_color'] = request.form['pack_color' + str(i)]
        #     i += 1
        for i in range(4):
            p = {}
            if 'patroller_name' + str(i) in request.form:
                p['patroller_name'] = request.form['patroller_name' + str(i)]
                p['call_sign'] = request.form['callsign' + str(i)]
                p['pack_color'] = request.form['packcolor' + str(i)]
                p['tent_color'] = request.form['tentcolor' + str(i)]
                p['fly_color'] = request.form['flycolor' + str(i)]
                p['supervision'] = request.form['supervision' + str(i)]
                p['planning'] = request.form['planning' + str(i)]
                p['contingency'] = request.form['contingency' + str(i)]
                p['comms'] = request.form['comms' + str(i)]
                p['team_selection'] = request.form['team_selection' + str(i)]
                p['fitness'] = request.form['fitness' + str(i)]
                p['env'] = request.form['env' + str(i)]
                p['complexity'] = request.form['complexity' + str(i)]
            else:
                p['patroller_name'] = ''
                p['call_sign'] = ''
                p['pack_color'] = ''
                p['tent_color'] = ''
                p['fly_color'] = ''
                p['supervision'] = ''
                p['planning'] = ''
                p['contingency'] = ''
                p['comms'] = ''
                p['team_selection'] = ''
                p['fitness'] = ''
                p['env'] = ''
                p['complexity'] = ''
            self.patrollers.append(p)

        self.day_plans = []
        for i in range(9):
            d_p = {}
            if 'date' + str(i) in request.form:
                d_p['date'] = request.form['date' + str(i)]
                d_p['starting_point'] = request.form['startingpoint' + str(i)]
                d_p['ending_point'] = request.form['endingpoint' + str(i)]
                d_p['route'] = request.form['route' + str(i)]
                d_p['mode'] = request.form['mode' + str(i)]
            else:
                d_p['date'] = ''
                d_p['starting_point'] = ''
                d_p['ending_point'] = ''
                d_p['route'] = ''
                d_p['mode'] = ''
            self.day_plans.append(d_p)

        self.cars = car_services.get_names()
        self.car_plate = self.request_dict.carplate
        self.car_make = self.request_dict.carmake
        self.car_model = self.request_dict.carmodel
        self.car_color = self.request_dict.carcolor
        self.car_location = self.request_dict.carlocation

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
        self.probe_pole = self.request_dict.probepole
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
        self.contact_work0 = self.request_dict.contactwork0
        self.contact_home0 = self.request_dict.contacthome0
        self.contact_cell0 = self.request_dict.contactcell0
        self.contact_email1 = self.request_dict.contactemail1
        self.contact_work1 = self.request_dict.contactwork1
        self.contact_home1 = self.request_dict.contacthome1
        self.contact_cell1 = self.request_dict.contactcell1

        self.s_avg = self.request_dict.savg
        self.p_avg = self.request_dict.pavg
        self.cr_avg = self.request_dict.cravg
        self.c_avg = self.request_dict.cavg
        self.ts_avg = self.request_dict.tsavg
        self.tf_avg = self.request_dict.tfavg
        self.e_avg = self.request_dict.eavg
        self.ic_avg = self.request_dict.icavg
        self.gar_avg = self.request_dict.garavg
        self.mitigated_avg = self.request_dict.mitigatedavg
        self.gar_mitigations = self.request_dict.garmitigations

        self.notes = self.request_dict.notes

    # def get_patrollers(self):
    #     pass

    def validate(self):
        self._validate_dates()

    def _validate_dates(self):
        if self.exit_date < self.entry_date:
            self.error = "Your exit date can't be before your entry date."

        if self.entry_date != self.day_plans[0]['date']:
            self.error = "Your days' plans should start on your entry date. " \
                         "The two dates don't match. You have days that are unaccounted for."

        for plan in reversed(self.day_plans):
            if plan['date'] != '':
                if self.exit_date != plan['date']:
                    self.error = "Your days' plans should end on your exit date. " \
                                 "The two dates don't match. You have days that are unaccounted for."
                break

        # if self.exit_date != self.day_plans[-1]['date']:
        #     self.error = "Your days' plans should end on your exit date. " \
        #                  "The two dates don't match. You have days that are unaccounted for."
