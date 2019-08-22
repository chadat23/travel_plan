import datetime

import sqlalchemy as sa

from travel_plan.models.modelbase import SqlAlchemyBasePatrol


class PatrolDay(SqlAlchemyBasePatrol):
    __tablename__ = 'patrol_days'
    # TODO: needs work
    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    created_date = sa.Column(sa.DateTime, default=datetime.datetime.now, index=True)

    date = sa.Column(sa.DateTime, nullable=False)
    starting_point = sa.Column(sa.Integer, sa.ForeignKey('patrols.id'))
    ending_point = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
    route = sa.Column(sa.String, index=True, unique=True, nullable=True)
    mode = sa.Column(sa.String, index=True)

    patrols = orm.relationship('PatrolUserUnit', backref='patroller')

    def __

    def __lt__(self, other):
        return self.name < other.name
