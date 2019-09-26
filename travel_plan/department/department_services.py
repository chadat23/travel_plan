from travel_plan import db
from travel_plan.department.departments import Department


def get_id_from_name(name: str):
    return db.session.query(Department.id).filter(Department.name == name).first()[0]
