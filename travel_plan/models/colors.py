import sqlalchemy as sa

from travel_plan.models.modelbase import SqlAlchemyBasePatrol


class Color(SqlAlchemyBasePatrol):
    __tablename__ = 'colors'

    id = sa.Column(sa.Integer, primary_key=True)
    name: str = sa.Column(sa.String, index=True, unique=True)

    def __lt__(self, other):
        return self.name < other.name
