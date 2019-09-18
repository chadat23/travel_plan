import datetime
import sqlalchemy as sa
from sqlalchemy import orm

from travel_plan.models.modelbase import SqlAlchemyBaseTravel
from travel_plan.models.travels import Travel
from travel_plan.services import color_services, user_services


class TravelUserUnit(SqlAlchemyBaseTravel):
    __tablename__ = 'travel_user_units'

    id = sa.Column(sa.Integer, primary_key=True)
    created_date = sa.Column(sa.DateTime, default=datetime.datetime.utcnow, index=True)

    travel_id: int = sa.Column(sa.Integer, sa.ForeignKey('travels.id'))
    user_id: int = sa.Column(sa.Integer, sa.ForeignKey('users.id'))

    call_sign: str = sa.Column(sa.String)

    # color_id: str = sa.Column(sa.String, sa.ForeignKey('colors.id'))
    # color = orm.relationship('Color', foreign_keys=[color_id])

    pack_color_id: str = sa.Column(sa.String, sa.ForeignKey('colors.id'))
    pack_color = orm.relationship('Color', foreign_keys=[pack_color_id])
    tent_color_id: str = sa.Column(sa.String, sa.ForeignKey('colors.id'))
    tent_color = orm.relationship('Color', foreign_keys=[tent_color_id])
    fly_color_id: str = sa.Column(sa.String, sa.ForeignKey('colors.id'))
    fly_color = orm.relationship('Color', foreign_keys=[fly_color_id])

    supervision: int = sa.Column(sa.Integer)
    planning: int = sa.Column(sa.Integer)
    contingency: int = sa.Column(sa.Integer)
    comms: int = sa.Column(sa.Integer)
    team_selection: int = sa.Column(sa.Integer)
    fitness: int = sa.Column(sa.Integer)
    env: int = sa.Column(sa.Integer)
    complexity: int = sa.Column(sa.Integer)
    total: int = sa.Column(sa.Integer)

    def __init__(self, traveler_name: str, call_sign: str,
                 pack_color: str, tent_color: str, fly_color: str,
                 supervision: int, planning: int, contingency: int, comms: int,
                 team_selection: int, fitness: int, env: int, complexity: int,
                 total: int):
        self.traveler = user_services.get_user_from_name(traveler_name)

        self.call_sign = call_sign

        print(pack_color)
        pack_color = color_services.add_if_not_present(pack_color)
        print(pack_color)
        self.pack_color_id = color_services.get_id_from_name(pack_color)
        tent_color = color_services.add_if_not_present(tent_color)
        self.tent_color_id = color_services.get_id_from_name(tent_color)
        fly_color = color_services.add_if_not_present(fly_color)
        self.fly_color_id = color_services.get_id_from_name(fly_color)

        self.supervision = supervision
        self.planning = planning
        self.contingency = contingency
        self.comms = comms
        self.team_selection = team_selection
        self.fitness = fitness
        self.env = env
        self.complexity = complexity
        self.total = total

    @property
    def total_gar_score(self):
        return (self.supervision + self.planning + self.contingency + self.comms
                + self.team_selection + self.fitness + self.env + self.complexity)
