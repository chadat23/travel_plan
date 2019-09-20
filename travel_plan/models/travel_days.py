from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import orm

from travel_plan.models.modelbase import SqlAlchemyBaseTravel
from travel_plan.services import location_services


class TravelDay(SqlAlchemyBaseTravel):
    __tablename__ = 'travel_days'
    # TODO: needs work
    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    created_date = sa.Column(sa.DateTime, default=datetime.now, index=True)

    travel_id: int = sa.Column(sa.Integer, sa.ForeignKey('travels.id'))

    date = sa.Column(sa.Date, nullable=False)
    starting_point_id = sa.Column(sa.Integer, sa.ForeignKey('locations.id'))
    starting_point = orm.relationship('Location', foreign_keys=[starting_point_id])
    ending_point_id = sa.Column(sa.Integer, sa.ForeignKey('locations.id'))
    ending_point = orm.relationship('Location', foreign_keys=[ending_point_id])
    route = sa.Column(sa.String, index=True)
    mode = sa.Column(sa.String, index=True)

    def __init__(self, date: str, starting_point: str, ending_point: str, route: str, mode: str):
        self.date = datetime.strptime(date, '%Y-%m-%d')
        self.starting_point_id = location_services.get_id_from_name(starting_point)
        self.ending_point_id = location_services.get_id_from_name(ending_point)
        self.route = route
        self.mode = mode

    def __lt__(self, other):
        return self.date < other.date

    def __repr__(self):
        return f'{str(self.date)} {self.starting_point} {self.ending_point} {self.route} {self.mode}'
