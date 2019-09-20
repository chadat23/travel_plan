import datetime
import enum

from travel_plan.app import db

# from travel_plan.models.modelbase import SqlAlchemyBaseTravel


class KindEnum(enum.Enum):
    Peak = 1
    Valley = 2
    River = 3
    Lake = 4
    Ridge = 5
    Trail_Head = 6
    Meadow = 7
    Other = 8
    Campground = 9


class Location(db.Model):
    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    name: str = db.Column(db.String, index=True, unique=True)
    latitude: float = db.Column(db.Float)
    longitude: float = db.Column(db.Float)
    kind: enum.Enum = db.Column(db.Enum(KindEnum))
    is_in_park: bool = db.Column(db.Boolean, nullable=False)
    note: str = db.Column(db.String)

    def __lt__(self, other):
        return self.name < other.name

    def __repr__(self):
        return f'{self.name}: {self.latitude}, {self.longitude}'

    def __init__(self, name: str, latitude: float, longitude: float,
                 kind: KindEnum = KindEnum.Other, note: str = "", is_in_park: bool = True):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.kind = kind
        self.is_in_park = is_in_park
        self.note = note

    # def __eq__(self, other):
    #     return self.name == other.name and self.latitude == other.latitude and self.longitude == other.longitude
