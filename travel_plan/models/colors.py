import sqlalchemy as sa

from travel_plan.models.modelbase import SqlAlchemyBaseTravel


class Color(SqlAlchemyBaseTravel):
    __tablename__ = 'colors'

    # id = sa.Column(sa.Integer, primary_key=True)
    id: str = sa.Column(sa.String, primary_key=True)

    def __init__(self, name: str):
        self.id = name.lower().strip().title()

    def __lt__(self, other):
        return self.id < other.id
