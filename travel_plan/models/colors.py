import sqlalchemy as sa

from travel_plan.models.modelbase import SqlAlchemyBasePatrol


class Color(SqlAlchemyBasePatrol):
    __tablename__ = 'colors'

    # id = sa.Column(sa.Integer, primary_key=True)
    id: str = sa.Column(sa.String, primary_key=True)

    def __init__(self, name: str):
        id = name.lower().strip().capitalize()

    def __lt__(self, other):
        return self.id < other.id
