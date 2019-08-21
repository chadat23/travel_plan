import datetime
import enum

# from sqlalchemy import Column, DateTime, Enum, Float, String
import sqlalchemy as sa

from travel_plan.models.modelbase import SqlAlchemyBasePatrol


class StatusEnum(enum.Enum):
    pending = 1
    rejected = 2


class ProposedLocation(SqlAlchemyBasePatrol):
    __tablename__ = 'proposed_locations'

    id = sa.Column(sa.Integer, primary_key=True)
    created_date = sa.Column(sa.DateTime, default=datetime.datetime.now)

    name: str = sa.Column(sa.String, primary_key=True, index=True)
    latitude: float = sa.Column(sa.Float)
    longitude: float = sa.Column(sa.Float)
    note: str = sa.Column(sa.String)
    status: enum.Enum = sa.Column(sa.Enum(StatusEnum), default=StatusEnum.pending)

    def __lt__(self, other):
        return self.name < other.name
