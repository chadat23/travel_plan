from typing import List, Optional

from passlib.handlers.sha2_crypt import sha512_crypt as crypto
from sqlalchemy.orm import Session

from travel_plan.config import NUMB_OF_HASHES
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


def get_user_from_email(email: str) -> Optional[User]:
    session: Session = db_session.create_session()

    try:
        return session.query(User).filter(User.email == email).first()
    except:
        return None
    finally:
        session.close()


def create_user(name: str, email: str, home_phone: str, work_phone: str, cell_phone: str, active: bool = True):
    user = User(name, email, home_phone, work_phone, cell_phone, active)

    session: Session = db_session.create_session()

    try:
        session.add(user)
    except:
        return None
    finally:
        session.close()


def update_user(user: User, active: bool, name: str = '', email: str = '',
                work_phone: str = '', home_phone: str = '', cell_phone: str = ''):
    updated = False
    if active != user.active:
        user.active = active
        updated = True
    if name and name != user.name:
        user.name = name
        updated = True
    if email and email != user.email:
        user.email = email
        updated = True
    if work_phone and work_phone != user.work_phone:
        user.work_phone = work_phone
        updated = True
    if home_phone and home_phone != user.home_phone:
        user.home_phone = home_phone
        updated = True
    if cell_phone and cell_phone != user.cell_phone:
        user.cell_phone = cell_phone
        updated = True

    if updated:
        session: Session = db_session.create_session()
        session.commit()
        session.close()

    return user
