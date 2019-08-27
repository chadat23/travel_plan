import datetime

# from sqlalchemy import Column, DateTime, Integer, String, orm
import sqlalchemy as sa
from sqlalchemy import orm

from travel_plan.models.modelbase import SqlAlchemyBasePatrol


class User(SqlAlchemyBasePatrol):
    __tablename__ = 'users'

    # TODO: lots (sa. and __init__)
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    created_date = sa.Column(sa.DateTime, default=datetime.datetime.now, index=True)

    name = sa.Column(sa.String, nullable=False)
    email = sa.Column(sa.String, index=True, unique=True, nullable=True)
    hashed_ssn = sa.Column(sa.String, index=True)

    patrols = orm.relationship('PatrolUserUnit', backref='patroller')

    active: bool = sa.Column(sa.Boolean, nullable=False)

    def __init__(self, name: str, email: str, hashed_ssn: str, active: bool = True):
        self.name = name
        self.email = email
        self.hashed_ssn = hashed_ssn
        self.active = active


    def __lt__(self, other):
        return self.name < other.name
