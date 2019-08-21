import datetime
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.orm import relationship

from travel_plan.models.modelbase import SqlAlchemyBasePatrol


class PatrolUnit(SqlAlchemyBasePatrol):
    __tablename__ = 'patrol_units'

    created_date = sa.Column(sa.DateTime, default=datetime.datetime.utcnow, index=True)

    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'), primary_key=True)
    user = orm.relation('User')
    patrol_id = sa.Column(sa.Integer, sa.ForeignKey('patrols.id'), primary_key=True)
    patrol = orm.relation('Patrol')
    pack_color = sa.Column(sa.String, sa.ForeignKey('colors.name'))
    tent_color = sa.Column(sa.String, sa.ForeignKey('colors.name'))
    fly_color = sa.Column(sa.String, sa.ForeignKey('colors.name'))
    leader = sa.Column(sa.Boolean, default=False)
