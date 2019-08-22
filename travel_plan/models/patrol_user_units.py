import datetime
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.orm import relationship

from travel_plan.models.modelbase import SqlAlchemyBasePatrol


class PatrolUserUnit(SqlAlchemyBasePatrol):
    __tablename__ = 'patrol_user_units'

    id = sa.Column(sa.Integer, primary_key=True)
    created_date = sa.Column(sa.DateTime, default=datetime.datetime.utcnow, index=True)

    patrol_id = sa.Column(sa.Integer, sa.ForeignKey('patrols.id'))
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
    pack_color = sa.Column(sa.String, sa.ForeignKey('colors.id'))
    # pack_color = orm.relationship('Color', foreign_keys=[pack_color_id])
    tent_color = sa.Column(sa.String, sa.ForeignKey('colors.id'))
    fly_color = sa.Column(sa.String, sa.ForeignKey('colors.id'))
