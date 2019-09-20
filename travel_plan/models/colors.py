import flask_sqlalchemy as sa

from travel_plan.models.modelbase import SqlAlchemyBaseTravel


class Color(SqlAlchemyBaseTravel):
    __tablename__ = 'colors'

    # id = sa.Column(sa.Integer, primary_key=True)
    id: str = sa.Column(sa.Integer, primary_key=True)
    name: str = sa.Column(sa.String)
    

    def __init__(self, name: str):
        self.name = name.lower().strip().title()

    def __lt__(self, other):
        return self.name < other.name
