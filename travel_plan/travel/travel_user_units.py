import datetime

from travel_plan import db
from travel_plan.user import user_services
from travel_plan.user.users import User
from travel_plan.color import color_services


class TravelUserUnit(db.Model):
    __tablename__ = 'travel_user_units'

    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, index=True)

    travel_id: int = db.Column(db.Integer, db.ForeignKey('travels.id'))
    user_id: int = db.Column(db.Integer, db.ForeignKey('users.id'))
    user: User = db.relationship('User', foreign_keys=[user_id])

    call_sign: str = db.Column(db.String)

    pack_color_id: int = db.Column(db.Integer, db.ForeignKey('colors.id'))
    pack_color = db.relationship('Color', foreign_keys=[pack_color_id])
    tent_color_id: int = db.Column(db.Integer, db.ForeignKey('colors.id'))
    tent_color = db.relationship('Color', foreign_keys=[tent_color_id])
    fly_color_id: int = db.Column(db.Integer, db.ForeignKey('colors.id'))
    fly_color = db.relationship('Color', foreign_keys=[fly_color_id])

    supervision: int = db.Column(db.Integer)
    planning: int = db.Column(db.Integer)
    contingency: int = db.Column(db.Integer)
    comms: int = db.Column(db.Integer)
    team_selection: int = db.Column(db.Integer)
    fitness: int = db.Column(db.Integer)
    env: int = db.Column(db.Integer)
    complexity: int = db.Column(db.Integer)
    total: int = db.Column(db.Integer)

    def __init__(self, traveler_name: str, call_sign: str,
                 pack_color: str, tent_color: str, fly_color: str,
                 supervision: int, planning: int, contingency: int, comms: int,
                 team_selection: int, fitness: int, env: int, complexity: int,
                 total: int):

        self.traveler = user_services.get_user_by_name(traveler_name)
        if not self.traveler:
            self.traveler = user_services.create_user(traveler_name, active=False)

        self.call_sign = call_sign

        if pack_color:
            pack_color = color_services.add_if_not_present(pack_color)
            self.pack_color_id = color_services.get_id_by_name(pack_color)
        if tent_color:
            tent_color = color_services.add_if_not_present(tent_color)
            self.tent_color_id = color_services.get_id_by_name(tent_color)
        if fly_color:
            fly_color = color_services.add_if_not_present(fly_color)
            self.fly_color_id = color_services.get_id_by_name(fly_color)

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
