import datetime
import enum

from sqlalchemy import Column, DateTime, Enum, Float, String

from travel_plan.sql_models.modelbase import SqlAlchemyBasePatrol


class StatusEnum(enum.Enum):
    pending = 1
    rejected = 2


class ProposedLocation(SqlAlchemyBasePatrol):
    __tablename__ = 'proposed_locations'

    created_date = Column(DateTime, default=datetime.datetime.now)

    name: str = Column(String, primary_key=True, index=True)
    latitude: float = Column(Float)
    longitude: float = Column(Float)
    note: str = Column(String)
    status: Enum = Column(Enum(StatusEnum), default=StatusEnum.pending)

    def __lt__(self, other):
        return self.name < other.name
