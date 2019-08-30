import datetime
import enum

import sqlalchemy as sa

from travel_plan.models.modelbase import SqlAlchemyBasePatrol

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


class Location(SqlAlchemyBasePatrol):
    __tablename__ = 'locations'

    id = sa.Column(sa.Integer, primary_key=True)
    created_date = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)

    name: str = sa.Column(sa.String, index=True, unique=True)
    latitude: float = sa.Column(sa.Float)
    longitude: float = sa.Column(sa.Float)
    kind: enum.Enum = sa.Column(sa.Enum(KindEnum))
    is_in_park: bool = sa.Column(sa.Boolean, nullable=False)
    note: str = sa.Column(sa.String)

    # patrols = relationship('Location', backref='visited', lazy=True)

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
