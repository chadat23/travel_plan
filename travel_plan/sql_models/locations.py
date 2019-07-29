import datetime
import sqlalchemy as sa
from travel_plan.sql_models.modelbase_existing import SqlAlchemyBaseExisting


class Location(SqlAlchemyBaseExisting):
    __tablename__ = 'locations'

    created_date = sa.Column(sa.DateTime, default=datetime.datetime.now)

    name: str = sa.Column(sa.String, primary_key=True, index=True)
    latitude: float = sa.Column(sa.Float)
    longitude: float = sa.Column(sa.Float)

    def __lt__(self, other):
        return self.name < other.name
