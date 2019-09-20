import datetime
from typing import List

import sqlalchemy as sa
import sqlalchemy.orm as orm

from travel_plan.models.cars import Car
from travel_plan.models.locations import Location
from travel_plan.models.modelbase import SqlAlchemyBaseTravel
from travel_plan.models.travel_days import TravelDay
from travel_plan.models.users import User

contact_association_table = sa.Table('travel_contact_association', SqlAlchemyBaseTravel.metadata,
                                     sa.Column('travels_id', sa.Integer, sa.ForeignKey('travels.id'), primary_key=True),
                                     sa.Column('contacts_id', sa.Integer, sa.ForeignKey('users.id'), primary_key=True)
                                     )


class Travel(SqlAlchemyBaseTravel):
    __tablename__ = 'travels'

    id = sa.Column(sa.Integer, primary_key=True)
    created_date = sa.Column(sa.DateTime, default=datetime.datetime.utcnow, index=True)

    start_date: datetime = sa.Column(sa.Date, index=True)
    entry_point_id = sa.Column(sa.Integer, sa.ForeignKey('locations.id'))
    entry_point: Location = orm.relationship('Location', foreign_keys=[entry_point_id])
    end_date: datetime = sa.Column(sa.Date, index=True)
    exit_point_id = sa.Column(sa.Integer, sa.ForeignKey('locations.id'))
    exit_point: Location = orm.relationship('Location', foreign_keys=[exit_point_id])

    tracked = sa.Column(sa.Boolean, index=False)
    plb = sa.Column(sa.String, index=False)

    trip_leader_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
    trip_leader = orm.relationship('User', foreign_keys=[trip_leader_id])

    travelers = orm.relationship('TravelUserUnit', backref='travel')
    travel_days: TravelDay = orm.relationship('TravelDay', backref='travel')

    car_id: int = sa.Column(sa.Integer, sa.ForeignKey('cars.id'))
    car: Car = orm.relationship('Car', foreign_keys=[car_id])
    car_location: str = sa.Column(sa.String)

    bivy_gear = sa.Column(sa.Boolean)
    compass = sa.Column(sa.Boolean)
    first_aid_kit = sa.Column(sa.Boolean)
    flagging = sa.Column(sa.Boolean)
    flare = sa.Column(sa.Boolean)
    flashlight = sa.Column(sa.Boolean)
    gps = sa.Column(sa.Boolean)
    head_lamp = sa.Column(sa.Boolean)
    helmet = sa.Column(sa.Boolean)
    ice_axe = sa.Column(sa.Boolean)
    map = sa.Column(sa.Boolean)
    matches = sa.Column(sa.Boolean)
    probe_pole = sa.Column(sa.Boolean)
    radio = sa.Column(sa.Boolean)
    rope = sa.Column(sa.Boolean)
    shovel = sa.Column(sa.Boolean)
    signal_mirror = sa.Column(sa.Boolean)
    space_blanket = sa.Column(sa.Boolean)
    spare_battery = sa.Column(sa.Boolean)
    tent = sa.Column(sa.Boolean)
    whistle = sa.Column(sa.Boolean)

    days_of_food = sa.Column(sa.Float)
    weapon = sa.Column(sa.String)
    radio_monitor_time = sa.Column(sa.String)
    off_trail_travel = sa.Column(sa.Boolean)
    cell_number = sa.Column(sa.String)
    satellite_number = sa.Column(sa.String)

    contacts: User = orm.relationship('User', secondary=contact_association_table)

    files: User = orm.relationship('TravelFile', backref='travel')

    gar_avg = sa.Column(sa.Float)
    mitigated_gar = sa.Column(sa.Float)
    gar_mitigations = sa.Column(sa.String)

    notes = sa.Column(sa.String)

    def __init__(self, start_date: datetime, entry_point_id: int, end_date: datetime, exit_point_id: int,
                 tracked: bool, plb: str, trip_leader_id: int, car_id: int, car_location: str,
                 bivy_gear: bool,
                 compass: bool,
                 first_aid_kit: bool,
                 flagging: bool,
                 flare: bool,
                 flashlight: bool,
                 gps: bool,
                 head_lamp: bool,
                 helmet: bool,
                 ice_axe: bool,
                 map: bool,
                 matches: bool,
                 probe_pole: bool,
                 radio: bool,
                 rope: bool,
                 shovel: bool,
                 signal_mirror: bool,
                 space_blanket: bool,
                 spare_battery: bool,
                 tent: bool,
                 whistle: bool,
                 days_of_food: float, weapon: str, radio_monitor_time: str, off_trail_travel: bool,
                 cell_number: str, satellite_number: str,
                 gar_avg: float, mitigated_gar: int, gar_mitigations: str,
                 notes: str,
                 ):
        self.start_date = start_date
        self.entry_point_id = entry_point_id
        self.end_date = end_date
        self.exit_point_id = exit_point_id

        self.tracked = tracked
        self.plb = plb

        self.trip_leader_id = trip_leader_id

        self.car_id = car_id
        self.car_location = car_location

        self.bivy_gear = bivy_gear
        self.compass = compass
        self.first_aid_kit = first_aid_kit
        self.flagging = flagging
        self.flare = flare
        self.flashlight = flashlight
        self.gps = gps
        self.head_lamp = head_lamp
        self.helmet = helmet
        self.ice_axe = ice_axe
        self.map = map
        self.matches = matches
        self.probe_pole = probe_pole
        self.radio = radio
        self.rope = rope
        self.shovel = shovel
        self.signal_mirror = signal_mirror
        self.space_blanket = space_blanket
        self.spare_battery = spare_battery
        self.tent = tent
        self.whistle = whistle

        self.days_of_food = days_of_food
        self.weapon = weapon
        self.radio_monitor_time = radio_monitor_time
        self.off_trail_travel = off_trail_travel
        self.cell_number = cell_number
        self.satellite_number = satellite_number

        self.gar_avg = float(gar_avg)
        self.mitigated_gar = float(mitigated_gar)
        self.gar_mitigations = gar_mitigations

        self.notes = notes

    def __repr__(self):
        return f'{self.start_date} - {self.entry_point}, {self.entry_point} - {self.exit_point}'
