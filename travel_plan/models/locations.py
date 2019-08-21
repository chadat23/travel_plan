import datetime
import sqlalchemy as sa

from travel_plan.models.modelbase import SqlAlchemyBasePatrol


class Location(SqlAlchemyBasePatrol):
    __tablename__ = 'locations'

    id = sa.Column(sa.Integer, primary_key=True)
    created_date = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)

    name: str = sa.Column(sa.String, index=True, unique=True)
    latitude: float = sa.Column(sa.Float)
    longitude: float = sa.Column(sa.Float)

    # patrols = relationship('Location', backref='visited', lazy=True)

    def __lt__(self, other):
        return self.name < other.name

    def __repr__(self):
        return f'{self.name}: {self.latitude}, {self.longitude}'

    # def __eq__(self, other):
    #     return self.name == other.name and self.latitude == other.latitude and self.longitude == other.longitude
