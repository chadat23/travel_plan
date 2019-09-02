from typing import List, Optional

from sqlalchemy.orm import Session

from travel_plan.models import db_session
from travel_plan.models.users import User


def get_users() -> List[User]:
    session: Session = db_session.create_session()

    try:
        return session.query(User).order_by(User.name).all()
    except:
        return []
    finally:
        session.close()


def get_names() -> List[str]:
    session: Session = db_session.create_session()

    try:
        return [n[0] for n in session.query(User.name).order_by(User.name).all()]
        # return session.query(User.name).order_by(User.name).all()
    except:
        return []
    finally:
        session.close()


def get_id_from_name(name: str) -> Optional[int]:
    session: Session = db_session.create_session()

    try:
        return session.query(User).filter(User.name == name).first().id
    except:
        return None
    finally:
        session.close()


def get_user_from_name(name: str) -> Optional[User]:
    session: Session = db_session.create_session()

    try:
        return session.query(User).filter(User.name == name).first()
    except:
        return None
    finally:
        session.close()
