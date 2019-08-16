import datetime
import sqlalchemy as sa
from sqlalchemy.orm import relationship

from travel_plan.sql_models.modelbase import SqlAlchemyBasePatrol


class Location(SqlAlchemyBasePatrol):
    __tablename__ = 'locations'

    created_date = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)

    name: str = sa.Column(sa.String, primary_key=True, index=True)
    latitude: float = sa.Column(sa.Float)
    longitude: float = sa.Column(sa.Float)

    # patrols = relationship('Location', backref='visited', lazy=True)

    def __lt__(self, other):
        return self.name < other.name

    def __repr__(self):
        return self.name
