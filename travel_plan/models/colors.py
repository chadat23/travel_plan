from travel_plan.app import db

from travel_plan.models.modelbase import SqlAlchemyBaseTravel


class Color(SqlAlchemyBaseTravel):
    __tablename__ = 'colors'

    # id = db.Column(db.Integer, primary_key=True)
    id: str = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String)
    

    def __init__(self, name: str):
        self.name = name.lower().strip().title()

    def __lt__(self, other):
        return self.name < other.name
