import datetime
from sqlalchemy import Column, DateTime, Float, String
from travel_plan.sql_models.modelbase_existing import SqlAlchemyBaseExisting


class Location(SqlAlchemyBaseExisting):
    __tablename__ = 'locations'

    created_date = Column(DateTime, default=datetime.datetime.now)

    name: str = Column(String, primary_key=True, index=True)
    latitude: float = Column(Float)
    longitude: float = Column(Float)

    def __lt__(self, other):
        return self.name < other.name
