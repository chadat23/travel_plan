import datetime

from sqlalchemy import Column, DateTime, Integer, String, orm

from travel_plan.models.modelbase import SqlAlchemyBasePatrol


class User(SqlAlchemyBasePatrol):
    __tablename__ = 'users'

    # TODO: lots (sa. and __init__)
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=datetime.datetime.now, index=True)

    name = Column(String, nullable=False)
    email = Column(String, index=True, unique=True, nullable=True)
    hashed_ssn = Column(String, index=True)

    patrols = orm.relationship('PatrolUserUnit', backref='patroller')

    def __lt__(self, other):
        return self.name < other.name
