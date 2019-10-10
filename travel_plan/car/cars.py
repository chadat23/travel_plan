import datetime

from travel_plan import db
from travel_plan.color import color_services
from travel_plan.department import department_services
from travel_plan.department.departments import Department


class Car(db.Model):
    __tablename__ = 'cars'

    id: int = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=datetime.datetime.now, index=True)
    plate: str = db.Column(db.String, unique=True, nullable=False)
    make: str = db.Column(db.String)
    model: str = db.Column(db.String)
    color_id: int = db.Column(db.String, db.ForeignKey('colors.id'))
    color = db.relationship('Color', foreign_keys=[color_id])
    location: str = db.Column(db.String)
    active: bool = db.Column(db.Boolean)
    department_id: int = db.Column(db.String, db.ForeignKey('departments.id'))
    department = db.relationship('Department', foreign_keys=[department_id])
    notes = db.relationship('Note', backref='car')

    def __init__(self, plate: str, make: str = None, model: str = None, color: str = None, 
                 location: str = None, active: bool = None, department: Department = None):
        self.plate = plate
        self.make = make
        self.model = model
        color = color_services.add_if_not_present(color)
        self.color_id = color_services.get_id_by_name(color)
        self.location = location
        self.active = active
        self.department_id = department_services.get_id_by_name(department) if department else None

    def __lt__(self, other):
        return str(self) < str(other)

    def __repr__(self):
        return f'{self.plate} {self.make} {self.model} {self.color.name} {self.location}'

    @property
    def name(self):
        return str(self)
