import datetime

import flask_sqlalchemy as sa
from flask_sqlalchemy import orm

from travel_plan.models.modelbase import SqlAlchemyBaseTravel


class TravelFile(SqlAlchemyBaseTravel):
    __tablename__ = 'travel_files'

    id: str = sa.Column(sa.Integer, primary_key=True)
    created_date = sa.Column(sa.DateTime, default=datetime.datetime.now)
    name: str = sa.Column(sa.String, unique=True, nullable=False, index=True)
    travel_id: int = sa.Column(sa.Integer, sa.ForeignKey('travels.id'))

    def __init__(self, name: str):
        self.name = name

    def __lt__(self, other):
        return self.name < other.name

    def __repr__(self):
        return self.name
