from typing import List, Optional

from flask_sqlalchemy.orm import Session

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


def create_user(name: str = '', email: str = '',
                work_number: str = '', home_number: str = '', cell_number: str = '', active: bool = True,
                user: User = None) -> Optional[User]:
    if not user:
        user = User(name, email, work_number, home_number, cell_number, active)

    session: Session = db_session.create_session()

    try:
        session.add(user)
        session.commit()
        return user
    except:
        return None
    finally:
        session.close()


def update_user(user_id: int, active: bool, name: str = '', email: str = '',
                work_number: str = '', home_number: str = '', cell_number: str = ''):
    session: Session = db_session.create_session()
    try:
        user = session.query(User).filter(User.id == user_id).first()
        if active != user.active:
            user.active = active
        if name and name != user.name:
            user.name = name
        if email and email != user.email:
            user.email = email
        if work_number and work_number != user.work_number:
            user.work_number = work_number
        if home_number and home_number != user.home_number:
            user.home_number = home_number
        if cell_number and cell_number != user.cell_number:
            user.cell_number = cell_number

        session.commit()
    finally:
        session.close()

    return user
