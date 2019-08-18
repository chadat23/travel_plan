import datetime

from sqlalchemy import Column, DateTime, Integer, String

from travel_plan.models.modelbase import SqlAlchemyBasePatrol


class Color(SqlAlchemyBasePatrol):
    __tablename__ = 'colors'

    name: str = Column(String, primary_key=True, index=True)

    def __lt__(self, other):
        return self.name < other.name
