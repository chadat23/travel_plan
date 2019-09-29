import datetime

from travel_plan import db
from travel_plan.car.cars import Car
from travel_plan.location.locations import Location
from travel_plan.travel.travel_days import TravelDay
from travel_plan.user.users import User

contact_association_table = db.Table('travel_contact_association', db.metadata,
                                     db.Column('travels_id', db.Integer, db.ForeignKey('travels.id'), primary_key=True),
                                     db.Column('contacts_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
                                     )


class Travel(db.Model):
    __tablename__ = 'travels'

    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, index=True)

    start_date: datetime = db.Column(db.Date, index=True)
    entry_point_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    entry_point: Location = db.relationship('Location', foreign_keys=[entry_point_id])
    end_date: datetime = db.Column(db.Date, index=True)
    exit_point_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    exit_point: Location = db.relationship('Location', foreign_keys=[exit_point_id])

    tracked = db.Column(db.Boolean, index=False)
    plb = db.Column(db.String, index=False)

    trip_leader_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    trip_leader = db.relationship('User', foreign_keys=[trip_leader_id])

    travelers = db.relationship('TravelUserUnit', backref='travel')
    travel_days: TravelDay = db.relationship('TravelDay', backref='travel')

    car_id: int = db.Column(db.Integer, db.ForeignKey('cars.id'))
    car: Car = db.relationship('Car', foreign_keys=[car_id])
    car_location: str = db.Column(db.String)

    bivy_gear = db.Column(db.Boolean)
    compass = db.Column(db.Boolean)
    first_aid_kit = db.Column(db.Boolean)
    flagging = db.Column(db.Boolean)
    flare = db.Column(db.Boolean)
    flashlight = db.Column(db.Boolean)
    gps = db.Column(db.Boolean)
    head_lamp = db.Column(db.Boolean)
    helmet = db.Column(db.Boolean)
    ice_axe = db.Column(db.Boolean)
    map = db.Column(db.Boolean)
    matches = db.Column(db.Boolean)
    probe_pole = db.Column(db.Boolean)
    radio = db.Column(db.Boolean)
    rope = db.Column(db.Boolean)
    shovel = db.Column(db.Boolean)
    signal_mirror = db.Column(db.Boolean)
    space_blanket = db.Column(db.Boolean)
    spare_battery = db.Column(db.Boolean)
    tent = db.Column(db.Boolean)
    whistle = db.Column(db.Boolean)

    days_of_food = db.Column(db.Float)
    weapon = db.Column(db.String)
    radio_monitor_time = db.Column(db.String)
    off_trail_travel = db.Column(db.Boolean)
    cell_number = db.Column(db.String)
    satellite_number = db.Column(db.String)

    contacts: User = db.relationship('User', secondary=contact_association_table)

    files: User = db.relationship('TravelFile', backref='travel')

    gar_avg = db.Column(db.Float)
    mitigated_gar = db.Column(db.Float)
    gar_mitigations = db.Column(db.String)

    notes = db.Column(db.String)

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
