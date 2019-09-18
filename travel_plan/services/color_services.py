from typing import List, Optional

from sqlalchemy.orm import Session

from travel_plan.models import db_session
from travel_plan.models.colors import Color


def get_names() -> List[str]:
    session: Session = db_session.create_session()

    try:
        names = [n[0] for n in session.query(Color.name).order_by(Color.name).all()]
    except:
        names = []
    finally:
        session.close()

    return names


def is_present(name: str) -> bool:
    name = name.lower().strip().title()

    session: Session = db_session.create_session()

    try:
        # TODO: this should be cleaned up: return True or False
        print('is present', str(session.query(Color).filter(Color.name == name).all()))
        return session.query(Color).filter(Color.name == name).all()
    except Exception as e:
        print('error', e)
        return None
    finally:
        session.close()


def add(name: str):
    name = name.lower().strip().title()
    print('1', name)

    session: Session = db_session.create_session()
    try:
        print('a', name)
        session.add(Color(name))
        print('b', name)
        session.commit()
        print('2', name)
        return name
    except:
        return None
    finally:
        session.close()


def add_if_not_present(name: str) -> Optional[str]:
    print('one', name)
    if not is_present(name):
        print('two', name)
        return add(name)

    print('three', name)
    return name.lower().strip().title()


def get_id_from_name(name: str) -> Optional[int]:
    print('5555555555555555', name)
    name = name.lower().strip().title()

    session: Session = db_session.create_session()

    try:
        return session.query(Color.id).filter(Color.name == name).first()[0]
    except:
        return None
    finally:
        session.close()