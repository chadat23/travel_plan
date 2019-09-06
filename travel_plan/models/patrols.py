import datetime

import sqlalchemy as sa
import sqlalchemy.orm as orm

from travel_plan.models.modelbase import SqlAlchemyBaseTravel


class Patrol(SqlAlchemyBaseTravel):
    __tablename__ = 'patrols'

    id = sa.Column(sa.Integer, primary_key=True)
    created_date = sa.Column(sa.DateTime, default=datetime.datetime.utcnow, index=True)

    start_date = sa.Column(sa.Date, index=True, unique=False, nullable=False)
    entry_point_id = sa.Column(sa.Integer, sa.ForeignKey('locations.id'))
    entry_point = orm.relationship('Location', foreign_keys=[entry_point_id])
    end_date = sa.Column(sa.Date, index=True, unique=False, nullable=False)
    exit_point_id = sa.Column(sa.Integer, sa.ForeignKey('locations.id'))
    exit_point = orm.relationship('Location', foreign_keys=[exit_point_id])

    tracked = sa.Column(sa.Boolean, index=False, unique=False, nullable=True)
    plb = sa.Column(sa.String, index=False, unique=False, nullable=True)

    trip_leader_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
    trip_leader = orm.relationship('User', foreign_keys=[trip_leader_id])

    patrollers = orm.relationship('PatrolUserUnit', backref='patrol')
    patrol_dayss = orm.relationship('PatrolDay', backref='patrol')

    car_id = sa.Column(sa.Integer, sa.ForeignKey('cars.id'))
    car = orm.relationship('Car', foreign_keys=[car_id])
    car_location = sa.Column(sa.String)

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
                 whistle: bool):

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

    def __repr__(self):
        return f'{self.start_date} - {self.entry_point}, {self.entry_point} - {self.exit_point}'

