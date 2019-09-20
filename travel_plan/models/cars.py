import datetime

# from travel_plan.models.modelbase import SqlAlchemyBaseTravel
from travel_plan.services import color_services

from travel_plan.app import db


class Car(db.Model):
    __tablename__ = 'cars'

    id: str = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=datetime.datetime.now, index=True)
    plate: str = db.Column(db.String, unique=True, nullable=False)
    make: str = db.Column(db.String, nullable=False)
    model: str = db.Column(db.String, nullable=False)
    color_id: str = db.Column(db.String, db.ForeignKey('colors.id'))
    color = db.relationship('Color', foreign_keys=[color_id])
    location: str = db.Column(db.String, nullable=False)
    active: bool = db.Column(db.Boolean, nullable=False)

    def __init__(self, plate: str, make: str, model: str, color: str, 
                 location: str = 'NA', active: bool = True):
        self.plate = plate
        self.make = make
        self.model = model
        color = color_services.add_if_not_present(color)
        self.color_id = color_services.get_id_from_name(color)
        self.location = location
        self.active = active

    def __lt__(self, other):
        return str(self) < str(other)

    def __repr__(self):
        return f'{self.plate} {self.make} {self.model} {self.color.name} {self.location}'

    @property
    def name(self):
        return str(self)
