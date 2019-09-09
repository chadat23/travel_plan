import datetime

# from sqlalchemy import Column, DateTime, Integer, String, orm
import sqlalchemy as sa
from sqlalchemy import orm

from travel_plan.models.modelbase import SqlAlchemyBaseTravel


class User(SqlAlchemyBaseTravel):
    __tablename__ = 'users'

    # TODO: lots (sa. and __init__)
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    created_date = sa.Column(sa.DateTime, default=datetime.datetime.now, index=True)

    name = sa.Column(sa.String, nullable=False)
    email = sa.Column(sa.String, index=True, unique=True, nullable=True)

    travels = orm.relationship('TravelUserUnit', backref='traveler')

    home_number = sa.Column(sa.String)
    work_number = sa.Column(sa.String)
    cell_number = sa.Column(sa.String)

    active: bool = sa.Column(sa.Boolean, nullable=False)

    def __init__(self, name: str, email: str, home_number: str, work_number: str, cell_number: str,
                 active: bool = True):
        self.name = name
        self.email = email
        self.home_number = home_number
        self.work_number = work_number
        self.cell_number = cell_number
        self.active = active

    def __lt__(self, other):
        return self.name < other.name
