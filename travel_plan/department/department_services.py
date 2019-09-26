from typing import Optional

from travel_plan import db
from travel_plan.department.departments import Department


def get_id_from_name(name: str) -> Optional[int]:
    try:
        if name:
            return db.session.query(Department.id).filter(Department.name == name).first()[0]
        else:
            return None
    except:
        return None
