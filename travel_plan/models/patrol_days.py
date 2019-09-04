from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import orm

from travel_plan.models.modelbase import SqlAlchemyBasePatrol
from travel_plan.services import location_services


class PatrolDay(SqlAlchemyBasePatrol):
    __tablename__ = 'patrol_days'
    # TODO: needs work
    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    created_date = sa.Column(sa.DateTime, default=datetime.now, index=True)

    date = sa.Column(sa.DateTime, nullable=False)
    starting_point = sa.Column(sa.Integer, sa.ForeignKey('locations.id'))
    ending_point = sa.Column(sa.Integer, sa.ForeignKey('locations.id'))
    route = sa.Column(sa.String, index=True, unique=True, nullable=True)
    mode = sa.Column(sa.String, index=True)

    patrols = orm.relationship('PatrolDay', backref='patrol_day')

    def __init__(self, date: str, starting_point: str, ending_point: str, route: str, mode: str):
        self.date = datetime.strptime(date, '%Y-%m-%d')
        self.starting_point = location_services.get_id_from_name(starting_point)
        self.ending_point = location_services.get_id_from_name(ending_point)
        self.route = route
        self.mode = mode

    # def __lt__(self, other):
    #     return self.name < other.name
