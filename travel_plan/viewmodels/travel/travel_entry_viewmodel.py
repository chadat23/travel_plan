from typing import List

import flask

from travel_plan.models.users import User
from travel_plan.services import user_services, location_services, color_services, car_services
from travel_plan.viewmodels.shared.viewmodelbase import ViewModelBase


class TravelEntryViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()

        self.start_date: str = self.request_dict.startdate
        self.entry_point: str = self.request_dict.entrypoint
        self.end_date: str = self.request_dict.enddate
        self.exit_point: str = self.request_dict.exitpoint

        self.tracked = self.request_dict.tracked == '' or self.request_dict.tracked == 'yes'
        self.plb: str = self.request_dict.plb

        self.locations: List[str] = location_services.get_names()
        self.users: List[User] = user_services.get_users()
        self.colors: List[str] = color_services.get_names()

        request = flask.request
        self.trip_leader_name = self.request_dict.travelername0
        self.travelers = []
        # i = 0
        # while 'traveler_name' + str(i) in request.form:
        #     p = {}
        #     p['traveler_name'] = request.form['traveler_name' + str(i)]
        #     p['call_sign'] = request.form['call_sign' + str(i)]
        #     p['pack_color'] = request.form['pack_color' + str(i)]
        #     i += 1
        for i in range(4):
            t = {}
            if 'travelername' + str(i) in request.form:
                t['traveler_name'] = request.form['travelername' + str(i)]
                t['call_sign'] = request.form['callsign' + str(i)]
                t['pack_color'] = request.form['packcolor' + str(i)]
                t['tent_color'] = request.form['tentcolor' + str(i)]
                t['fly_color'] = request.form['flycolor' + str(i)]
                t['supervision'] = request.form['supervision' + str(i)]
                t['planning'] = request.form['planning' + str(i)]
                t['contingency'] = request.form['contingency' + str(i)]
                t['comms'] = request.form['comms' + str(i)]
                t['team_selection'] = request.form['teamselection' + str(i)]
                t['fitness'] = request.form['fitness' + str(i)]
                t['env'] = request.form['env' + str(i)]
                t['complexity'] = request.form['complexity' + str(i)]
                t['total'] = request.form['total' + str(i)]
            else:
                t['traveler_name'] = ''
                t['call_sign'] = ''
                t['pack_color'] = ''
                t['tent_color'] = ''
                t['fly_color'] = ''
                t['supervision'] = ''
                t['planning'] = ''
                t['contingency'] = ''
                t['comms'] = ''
                t['team_selection'] = ''
                t['fitness'] = ''
                t['env'] = ''
                t['complexity'] = ''
                t['total'] = ''
            self.travelers.append(t)

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

        self.contacts = []
        for i in range(2):
            c = {}
            if 'contactemail' + str(i) in request.form:
                c['contact_email'] = request.form['contactemail' + str(i)]
                c['contact_work'] = request.form['contactwork' + str(i)]
                c['contact_home'] = request.form['contacthome' + str(i)]
                c['contact_cell'] = request.form['contactcell' + str(i)]
            else:
                c['contact_email'] = ''
                c['contact_work'] = ''
                c['contact_home'] = ''
                c['contact_cell'] = ''
            self.contacts.append(c)

        self.cars = car_services.get_names()
        # self.cars = ['one', 'two']
        self.car_plate = self.request_dict.carplate
        self.car_make = self.request_dict.carmake
        self.car_model = self.request_dict.carmodel
        self.car_color = self.request_dict.carcolor
        self.car_location = self.request_dict.carlocation

        self.bivy_gear = self.request_dict.bivygear == 'on'
        self.compass = self.request_dict.compass == 'on'
        self.first_aid_kit = self.request_dict.firstaidkit == 'on'
        self.flagging = self.request_dict.flagging == 'on'
        self.flare = self.request_dict.flare == 'on'
        self.flashlight = self.request_dict.flashlight == 'on'
        self.gps = self.request_dict.gps == 'on'
        self.head_lamp = self.request_dict.headlamp == 'on'
        self.helmet = self.request_dict.helmet == 'on'
        self.ice_axe = self.request_dict.iceaxe == 'on'
        self.map = self.request_dict.map == 'on'
        self.matches = self.request_dict.matches == 'on'
        self.probe_pole = self.request_dict.probepole == 'on'
        self.radio = self.request_dict.radio == 'on'
        self.rope = self.request_dict.rope == 'on'
        self.shovel = self.request_dict.shovel == 'on'
        self.signal_mirror = self.request_dict.signalmirror == 'on'
        self.space_blanket = self.request_dict.spaceblanket == 'on'
        self.spare_battery = self.request_dict.sparebattery == 'on'
        self.tent = self.request_dict.tent == 'on'
        self.whistle = self.request_dict.whistle == 'on'

        self.days_of_food = self.request_dict.daysoffood
        self.weapon = self.request_dict.weapon
        self.radio_monitor_time = self.request_dict.radiomonitortime
        self.off_trail_travel = self.request_dict.offtrailtravel == '' or self.request_dict.offtrailtravel == 'yes'
        self.uploaded_files = ''
        if 'fileupload' in request.files:
            self.uploaded_files = request.files.getlist('fileupload')
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

        self.gar_avg = self.request_dict.garavg
        self.mitigated_gar = self.request_dict.mitigatedgar
        self.gar_mitigations = self.request_dict.garmitigations

        self.notes = self.request_dict.notes

    def validate(self):
        self._validate_dates()

        self._validate_fields()

    def _validate_fields(self):
        # if it's reported that there'll be off trail travel then there should be uploaded files
        if self.uploaded_files:
            file_name_1 = self.uploaded_files[0].filename
        else:
            file_name_1 = ''
        if (self.off_trail_travel and (not file_name_1)) or (not self.off_trail_travel and file_name_1):
            self.error = "Either you should select that you'll be traveling off trail and select files to upload, " \
                         "or have neither of those. Sorry, there's no present way to un-select the files."

        # Validate that logical traveler/gar fields make sense
        for t in self.travelers:
            if t['traveler_name']:
                for v in t.values():
                    if not v:
                        self.error = "All fields must be filled in for each traveler and each accompanying GAR score."
                        return

    def _validate_dates(self):
        if self.end_date < self.start_date:
            self.error = "Your exit date can't be before your entry date."

        if self.start_date != self.day_plans[0]['date']:
            self.error = "Your days' plans should start on your entry date. " \
                         "The two dates don't match. You have days that are unaccounted for."

        for plan in reversed(self.day_plans):
            if plan['date'] != '':
                if self.end_date != plan['date']:
                    self.error = "Your days' plans should end on your exit date. " \
                                 "The two dates don't match. You have days that are unaccounted for."
                break
