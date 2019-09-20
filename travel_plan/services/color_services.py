from typing import List, Optional

from flask_sqlalchemy.orm import Session

from travel_plan.models import db_session
from travel_plan.models.colors import Color


def get_names() -> List[str]:
    session: Session = db_session.create_session()

    try:
        return list(dict.fromkeys([n[0] for n in session.query(Color.name).order_by(Color.name).all()]))
        # names = set([n[0] for n in session.query(Color.name).order_by(Color.name).all()])
    except:
        return []
    finally:
        session.close()


def is_present(name: str) -> bool:
    name = name.lower().strip().title()

    session: Session = db_session.create_session()

    try:
        return session.query(Color).filter(Color.name == name).all() != []
    except Exception as e:
        print('Exception: ', e)
        return None
    finally:
        session.close()


def add(name: str):
    name = name.lower().strip().title()

    session: Session = db_session.create_session()
    try:
        session.add(Color(name))
        session.commit()
        return name
    except:
        return None
    finally:
        session.close()


def add_if_not_present(name: str) -> Optional[str]:
    if not is_present(name):
        return add(name)

    return name.lower().strip().title()


def get_id_from_name(name: str) -> Optional[int]:
    name = name.lower().strip().title()

    session: Session = db_session.create_session()

    try:
        return session.query(Color.id).filter(Color.name == name).first()[0]
    except:
        return None
    finally:
        session.close()