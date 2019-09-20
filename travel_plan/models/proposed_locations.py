import datetime
import enum

from travel_plan.app import db

from travel_plan.models.modelbase import SqlAlchemyBaseTravel


class StatusEnum(enum.Enum):
    pending = 1
    rejected = 2


class ProposedLocation(SqlAlchemyBaseTravel):
    __tablename__ = 'proposed_locations'

    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=datetime.datetime.now)

    name: str = db.Column(db.String, primary_key=True, index=True)
    latitude: float = db.Column(db.Float)
    longitude: float = db.Column(db.Float)
    note: str = db.Column(db.String)
    status: enum.Enum = db.Column(db.Enum(StatusEnum), default=StatusEnum.pending)

    def __lt__(self, other):
        return self.name < other.name
