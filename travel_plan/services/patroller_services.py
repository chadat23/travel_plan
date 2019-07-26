from typing import List

from sqlalchemy.orm import Session

from travel_plan.nosql_models.patroller import Patroller
from travel_plan.sql_models import db_session
from travel_plan.sql_models.user import User


def all_patrollers():
    session: Session = db_session.create_session()
    try:
        users = list(session.query(User))
        users = {u.name: u for u in users}
    except:
        users = dict()
    finally:
        session.close()

    patrollers = {p.name: p for p in list(Patroller.objects())}

    for k, v in patrollers.items():
        if k not in users:
            users[k] = v

    return users

