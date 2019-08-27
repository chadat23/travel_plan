import sqlalchemy as sa
from sqlalchemy import orm

from travel_plan.models.modelbase import SqlAlchemyBasePatrol


class Car(SqlAlchemyBasePatrol):
    __tablename__ = 'cars'

    id: str = sa.Column(sa.Integer, primary_key=True)
    plate: str = sa.Column(sa.String, unique=True, nullable=False)
    make: str = sa.Column(sa.String, nullable=False)
    model: str = sa.Column(sa.String, nullable=False)
    color: str = sa.Column(sa.String, sa.ForeignKey('colors.id'))
    location: str = sa.Column(sa.String, nullable=False)
    active: bool = sa.Column(sa.Boolean, nullable=False)

    def __init__(self, plate: str, make: str, model: str, color: str, location: str, active: bool = True):
        self.plate = plate
        self.make = make
        self.model = model
        self.color = color
        self.location = location
        self.active = active

    def __lt__(self, other):
        return str(self) < str(other)

    def __repr__(self):
        return f'{self.plate} {self.make} {self.model} {self.color} {self.location}'

    @property
    def name(self):
        return str(self)
