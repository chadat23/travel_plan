import datetime
from travel_plan.app import db

from travel_plan.models.modelbase import SqlAlchemyBaseTravel


class TravelUserContact(SqlAlchemyBaseTravel):
    __tablename__ = 'travel_user_contacts'

    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, index=True)

    travel_id: int = db.Column(db.Integer, db.ForeignKey('travels.id'))
    user_id: int = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, travel_id: int, contact_id: int):
        # self.travel = travel
        self.travel_id = travel_id
        self.user_id = contact_id
