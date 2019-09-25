from typing import List, Optional

from travel_plan import db
from travel_plan.models.users import User


def get_users() -> List[User]:
    try:
        return db.session.query(User).order_by(User.name).all()
    except:
        return []


def get_names() -> List[str]:
    try:
        return [n[0] for n in db.session.query(User.name).order_by(User.name).all()]
        # return session.query(User.name).order_by(User.name).all()
    except:
        return []


def get_id_from_name(name: str) -> Optional[int]:
    try:
        return db.session.query(User).filter(User.name == name).first().id
    except:
        return None


def get_user_from_name(name: str) -> Optional[User]:
    try:
        return db.session.query(User).filter(User.name == name).first()
    except:
        return None


def get_user_from_email(email: str) -> Optional[User]:
    try:
        return db.session.query(User).filter(User.email == email).first()
    except:
        return None


def create_user(name: str = '', email: str = '',
                work_number: str = '', home_number: str = '', cell_number: str = '', department: str = "Unknown", active: bool = True,
                user: User = None) -> Optional[User]:
    if not user:
        user = User(name, email, work_number, home_number, cell_number, department, active)

    try:
        db.session.add(user)
        db.session.commit()
        return user
    except:
        return None


def update_user(user_id: int, active: bool, name: str = '', email: str = '',
                work_number: str = '', home_number: str = '', cell_number: str = ''):

    user = db.session.query(User).filter(User.id == user_id).first()
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

    db.session.commit()

    return user
