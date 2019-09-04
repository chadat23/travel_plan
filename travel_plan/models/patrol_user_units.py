import datetime
import sqlalchemy as sa
from sqlalchemy import orm

from travel_plan.models.modelbase import SqlAlchemyBasePatrol
from travel_plan.models.patrols import Patrol
from travel_plan.services import color_services, user_services


class PatrolUserUnit(SqlAlchemyBasePatrol):
    __tablename__ = 'patrol_user_units'

    id = sa.Column(sa.Integer, primary_key=True)
    created_date = sa.Column(sa.DateTime, default=datetime.datetime.utcnow, index=True)

    patrol_id: int = sa.Column(sa.Integer, sa.ForeignKey('patrols.id'))
    user_id: int = sa.Column(sa.Integer, sa.ForeignKey('users.id'))

    call_sign: str = sa.Column(sa.String)

    pack_color: str = sa.Column(sa.String, sa.ForeignKey('colors.id'))
    tent_color: str = sa.Column(sa.String, sa.ForeignKey('colors.id'))
    fly_color: str = sa.Column(sa.String, sa.ForeignKey('colors.id'))

    supervision: int = sa.Column(sa.Integer)
    planning: int = sa.Column(sa.Integer)
    contingency: int = sa.Column(sa.Integer)
    comms: int = sa.Column(sa.Integer)
    team_selection: int = sa.Column(sa.Integer)
    fitness: int = sa.Column(sa.Integer)
    env: int = sa.Column(sa.Integer)
    complexity: int = sa.Column(sa.Integer)

    def __init__(self, patroller_name: str, call_sign: str,
                 pack_color: str, tent_color: str, fly_color: str,
                 supervision: int, planning: int, contingency: int, comms: int,
                 team_selection: int, fitness: int, env: int, complexity: int):
        # self.patrol = patrol
        self.patroller = user_services.get_user_from_name(patroller_name)

        self.call_sign = call_sign

        #TODO: should be some sort of list of colors
        pack_color = pack_color.lower().strip().capitalize()
        color_services.add_if_not_present(pack_color)
        self.pack_color = pack_color
        tent_color = tent_color.lower().strip().capitalize()
        color_services.add_if_not_present(tent_color)
        self.tent_color = tent_color
        fly_color = fly_color.lower().strip().capitalize()
        color_services.add_if_not_present(fly_color)
        self.fly_color = fly_color

        self.supervision = supervision
        self.planning = planning
        self.contingency = contingency
        self.comms = comms
        self.team_selection = team_selection
        self.fitness = fitness
        self.env = env
        self.complexity = complexity

    @property
    def total_gar_score(self):
        return (self.supervision + self.planning + self.contingency + self.comms
                + self.team_selection + self.fitness + self.env + self.complexity)
