import datetime

from flask_sqlalchemy import Column, DateTime, Integer, String

from travel_plan.models.modelbase import SqlAlchemyBaseExternal


class User(SqlAlchemyBaseExternal):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=datetime.datetime.now, index=True)

    name = Column(String, nullable=False)
    email = Column(String, index=True, unique=True, nullable=True)
    hashed_ssn = Column(String, index=True)
