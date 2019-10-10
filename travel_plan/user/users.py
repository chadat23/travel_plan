import datetime

from travel_plan import db
# from travel_plan.models.travel_user_units import TravelUserUnit
from travel_plan.department.departments import Department
from travel_plan.department import department_services


class User(db.Model):
    __tablename__ = 'users'

    # TODO: lots (db. and __init__)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_date = db.Column(db.DateTime, default=datetime.datetime.now, index=True)

    name = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, unique=True)
    department_id: int = db.Column(db.String, db.ForeignKey('departments.id'))
    department: Department = db.relationship('Department', foreign_keys=[department_id])

    travels = db.relationship('TravelUserUnit', backref='traveler')

    home_number = db.Column(db.String)
    work_number = db.Column(db.String)
    cell_number = db.Column(db.String)

    active: bool = db.Column(db.Boolean, nullable=False)

    def __init__(self, name: str, email: str, 
                 work_number: str = None, home_number: str = None, cell_number: str = None,
                 department: str = None, active: bool = None):
        self.name = name
        self.email = email
        self.work_number = work_number
        self.home_number = home_number
        self.cell_number = cell_number
        self.active = active
        department_id = department_services.get_id_from_name(department)
        self.department_id = department_id

    def __lt__(self, other):
        return self.name < other.name

    def __eq__(self, other):
        return self.name == other.name and \
               self.email == other.email and \
               self.work_number == self.work_number and \
               self.home_number == self.home_number and \
               self.cell_number == self.cell_number and \
               self.department == self.department
