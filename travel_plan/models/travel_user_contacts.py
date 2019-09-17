import datetime
import sqlalchemy as sa
from sqlalchemy import orm

from travel_plan.models.modelbase import SqlAlchemyBaseTravel


class TravelUserContact(SqlAlchemyBaseTravel):
    __tablename__ = 'travel_user_contacts'

    id = sa.Column(sa.Integer, primary_key=True)
    created_date = sa.Column(sa.DateTime, default=datetime.datetime.utcnow, index=True)

    travel_id: int = sa.Column(sa.Integer, sa.ForeignKey('travels.id'))
    user_id: int = sa.Column(sa.Integer, sa.ForeignKey('users.id'))

    def __init__(self, travel_id: int, contact_id: int):
        # self.travel = travel
        self.travel_id = travel_id
        self.user_id = contact_id
