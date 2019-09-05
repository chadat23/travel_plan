from typing import List, Optional

from sqlalchemy.orm import Session

from travel_plan.models import db_session
from travel_plan.models.colors import Color


def get_names() -> List[str]:
    session: Session = db_session.create_session()

    try:
        names = [n[0] for n in session.query(Color.id).order_by(Color.id).all()]
    except:
        names = []
    finally:
        session.close()

    return names


def is_present(name: str) -> bool:
    name = name.lower().strip().capitalize()

    session: Session = db_session.create_session()

    try:
        return session.query(Color).filter(Color.id == name).all()
    except:
        return None
    finally:
        session.close()


def add(name: str):
    name = name.lower().strip().capitalize()

    session: Session = db_session.create_session()
    try:
        session.add(Color(name))
        session.commit()
        return name
    except:
        return None
    finally:
        session.close()


def add_if_not_present(name: str):
    name = name.lower().strip().capitalize()
    if not is_present(name):
        return add(name)

    return name