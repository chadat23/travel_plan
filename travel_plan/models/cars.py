import datetime
import enum

import sqlalchemy as sa
from sqlalchemy import orm

from travel_plan.models.modelbase import SqlAlchemyBaseTravel
from travel_plan.services import color_services

class DepartmentEnum(enum.Enum):
    Wilderness = 1
    BnG = 2


class Car(SqlAlchemyBaseTravel):
    __tablename__ = 'cars'

    id: str = sa.Column(sa.Integer, primary_key=True)
    created_date = sa.Column(sa.DateTime, default=datetime.datetime.now, index=True)
    plate: str = sa.Column(sa.String, unique=True, nullable=False)
    make: str = sa.Column(sa.String)
    model: str = sa.Column(sa.String)
    color_id: str = sa.Column(sa.String, sa.ForeignKey('colors.id'))
    color = orm.relationship('Color', foreign_keys=[color_id])
    location: str = sa.Column(sa.String)
    active: bool = sa.Column(sa.Boolean)
    department: str = sa.Column(sa.String)

    def __init__(self, plate: str, make: str = None, model: str = None, color: str = None, 
                 location: str = None, active: bool = None):
        self.plate = plate
        self.make = make
        self.model = model
        color = color_services.add_if_not_present(color)
        self.color_id = color_services.get_id_from_name(color)
        self.location = location
        self.active = active

    def __lt__(self, other):
        return str(self) < str(other)

    def __repr__(self):
        return f'{self.plate} {self.make} {self.model} {self.color.name} {self.location}'

    @property
    def name(self):
        return str(self)
