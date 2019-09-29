from typing import Optional

from travel_plan import db
from travel_plan.department.departments import Department


def get_id_from_name(name: str) -> Optional[int]:
    '''
    Get the id of the Department who's name matches the supplied name.

    :param name: the name of the Department to be queried
    :type name: str
    :return: an int if the name is found, otherwise None
    '''
    try:
        return db.session.query(Department.id).filter(Department.name == name).first()[0]
    except:
        return None
