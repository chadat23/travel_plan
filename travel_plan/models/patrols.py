import datetime

import sqlalchemy as sa
import sqlalchemy.orm as orm

from travel_plan.models.modelbase import SqlAlchemyBasePatrol


class Patrol(SqlAlchemyBasePatrol):
    __tablename__ = 'patrols'

    id = sa.Column(sa.Integer, primary_key=True)
    created_date = sa.Column(sa.DateTime, default=datetime.datetime.utcnow, index=True)

    start_date = sa.Column(sa.Date, index=True, unique=False, nullable=False)
    entry_point_id = sa.Column(sa.Integer, sa.ForeignKey('locations.id'))
    entry_point = orm.relationship('Location', foreign_keys=[entry_point_id])
    end_date = sa.Column(sa.Date, index=True, unique=False, nullable=False)
    exit_point_id = sa.Column(sa.Integer, sa.ForeignKey('locations.id'))
    exit_point = orm.relationship('Location', foreign_keys=[exit_point_id])

    tracked = sa.Column(sa.Boolean, index=False, unique=False, nullable=True)
    plb = sa.Column(sa.String, index=False, unique=False, nullable=True)

    trip_leader_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
    trip_leader = orm.relationship('User', foreign_keys=[trip_leader_id])

    patrollers = orm.relationship('PatrolUserUnit', backref='patrol')

    car_id = sa.Column(sa.Integer, sa.ForeignKey('cars.id'))
    car = orm.relationship('Car', foreign_keys=[car_id])
    car_location = sa.Column(sa.String)

    def __init__(self, start_date: datetime, entry_point_id: int, end_date: datetime, exit_point_id: int, 
                 tracked: bool, plb: str, trip_leader_id: int, car_id: int, car_location: str):

        self.start_date = start_date
        self.entry_point_id = entry_point_id
        self.end_date = end_date
        self.exit_point_id = exit_point_id

        self.tracked = tracked
        self.plb = plb

        self.trip_leader_id = trip_leader_id

        self.car_id = car_id
        self.car_location = car_location

    def __repr__(self):
        return f'{self.start_date} - {self.entry_point}, {self.entry_point} - {self.exit_point}'

