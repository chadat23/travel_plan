import datetime

from sqlalchemy import Column, DateTime, Integer, String, orm

from travel_plan.sql_models.modelbase import SqlAlchemyBasePatrol


class User(SqlAlchemyBasePatrol):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=datetime.datetime.now, index=True)

    name = Column(String, nullable=False)
    email = Column(String, index=True, unique=True, nullable=True)
    hashed_ssn = Column(String, index=True)

    patrol_units = orm.relation("PatrolUnit", back_populates='user')

    def __lt__(self, other):
        return self.name < other.name
