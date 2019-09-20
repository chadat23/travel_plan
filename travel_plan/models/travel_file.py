import datetime

from travel_plan.app import db

from travel_plan.models.modelbase import SqlAlchemyBaseTravel


class TravelFile(SqlAlchemyBaseTravel):
    __tablename__ = 'travel_files'

    id: str = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=datetime.datetime.now)
    name: str = db.Column(db.String, unique=True, nullable=False, index=True)
    travel_id: int = db.Column(db.Integer, db.ForeignKey('travels.id'))

    def __init__(self, name: str):
        self.name = name

    def __lt__(self, other):
        return self.name < other.name

    def __repr__(self):
        return self.name
