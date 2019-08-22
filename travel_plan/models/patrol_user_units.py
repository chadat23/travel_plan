import datetime
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.orm import relationship

from travel_plan.models.modelbase import SqlAlchemyBasePatrol
from travel_plan.models.patrols import Patrol
from travel_plan.services import user_services 


class PatrolUserUnit(SqlAlchemyBasePatrol):
    __tablename__ = 'patrol_user_units'

    id = sa.Column(sa.Integer, primary_key=True)
    created_date = sa.Column(sa.DateTime, default=datetime.datetime.utcnow, index=True)

    patrol_id = sa.Column(sa.Integer, sa.ForeignKey('patrols.id'))
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
    pack_color = sa.Column(sa.String, sa.ForeignKey('colors.id'))
    tent_color = sa.Column(sa.String, sa.ForeignKey('colors.id'))
    fly_color = sa.Column(sa.String, sa.ForeignKey('colors.id'))

    def __init__(self, patrol: Patrol, patroller_name: str, pack_color: str, tent_color: str, fly_color: str):
        self.patrol = patrol
        self.patroller = user_services.get_user_from_name(patroller_name)
        self.pack_color = pack_color
        self.tent_color = tent_color
        self.fly_color = fly_color
