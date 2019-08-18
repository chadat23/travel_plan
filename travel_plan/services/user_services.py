from typing import List

from sqlalchemy.orm import Session

from travel_plan.models import db_session
from travel_plan.models.users import User


def all_patrollers() -> List[User]:
    session: Session = db_session.create_session_external()
    try:
        users = list(session.query(User))
    except:
        users = dict()
    finally:
        session.close()

    return users
