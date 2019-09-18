import datetime

import sqlalchemy as sa
from sqlalchemy import orm

from travel_plan.models.modelbase import SqlAlchemyBaseTravel
from travel_plan.services import color_services


class Car(SqlAlchemyBaseTravel):
    __tablename__ = 'cars'

    id: str = sa.Column(sa.Integer, primary_key=True)
    created_date = sa.Column(sa.DateTime, default=datetime.datetime.now, index=True)
    plate: str = sa.Column(sa.String, unique=True, nullable=False)
    make: str = sa.Column(sa.String, nullable=False)
    model: str = sa.Column(sa.String, nullable=False)
    color: str = sa.Column(sa.String, sa.ForeignKey('colors.id'))
    location: str = sa.Column(sa.String, nullable=False)
    active: bool = sa.Column(sa.Boolean, nullable=False)

    def __init__(self, plate: str, make: str, model: str, color: str, 
                 location: str = 'NA', active: bool = True):
        self.plate = plate
        self.make = make
        self.model = model
        self.color = color_services.add_if_not_present(color)
        self.location = location
        self.active = active

    def __lt__(self, other):
        return str(self) < str(other)

    def __repr__(self):
        return f'{self.plate} {self.make} {self.model} {self.color} {self.location}'

    @property
    def name(self):
        return str(self)
