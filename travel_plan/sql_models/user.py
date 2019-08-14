import datetime

from sqlalchemy import Column, DateTime, Integer, String

from travel_plan.sql_models.modelbase_existing import SqlAlchemyBaseExisting


class User(SqlAlchemyBaseExisting):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=datetime.datetime.now, index=True)

    name = Column(String, nullable=False)
    email = Column(String, index=True, unique=True, nullable=True)
