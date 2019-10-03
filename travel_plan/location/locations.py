import datetime
import enum

import sqlalchemy as sa
import sqlalchemy.orm as orm

from travel_plan import db


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
    Basin = 10
    Area = 11


location_association_table = sa.Table('location_alias_association', db.Model.metadata,
                                      db.Column('location_1_id', db.Integer, db.ForeignKey('locations.id'),
                                                primary_key=True),
                                      db.Column('location_2_id', db.Integer, db.ForeignKey('locations.id'),
                                                primary_key=True)
                                      )


class Location(db.Model):
    '''
    An object representing a named location.

    Since some geographic locations have multiple names, or are 
    sufficiently close to be all but geographically
    indistinguishable, multiple Locations may refer to the same
    geogrphic location. Aliasses are used to track and account
    for this.

    :param name: the name of the location
    :type name: str
    :param latitude: the latitude of the location
    :type name: float
    :param longitude: the longitude of the location
    :type name: float
    :param kind: what the location is: lake, river, peak, 
    trailhead, campground, etc.
    :type kind: KindEnum
    :param note: Any notes deemed relevant for the location.
    :type note: str
    :param is_in_park: whether or not the location is in the park
    True for yes, False for no
    :type is_in_park: bool
    :param aliases: other Locations that go by the same name
    :type aliases: int
    '''
    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    name: str = db.Column(db.String, index=True, unique=True, nullable=False)
    latitude: float = db.Column(db.Float)
    longitude: float = db.Column(db.Float)
    kind: enum.Enum = db.Column(db.Enum(KindEnum))
    is_in_park: bool = db.Column(db.Boolean)
    aliases: int = db.relationship('Location', secondary=location_association_table,
                                   primaryjoin=id == location_association_table.c.location_1_id,
                                   secondaryjoin=id == location_association_table.c.location_1_id,
                                   )
    note: str = db.Column(db.String)

    def __init__(self, name: str, latitude: float = None, longitude: float = None,
                 kind: KindEnum = None, note: str = None, is_in_park: bool = None):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.kind = kind
        self.is_in_park = is_in_park
        self.note = note

    def __lt__(self, other):
        return self.name < other.name

    def __repr__(self):
        return f'{self.name}: {self.latitude}, {self.longitude}'

    # def __eq__(self, other):
    #     return self.name == other.name and self.latitude == other.latitude and self.longitude == other.longitude
