from typing import List, Optional

from sqlalchemy.orm import Session

from travel_plan import db
from travel_plan.models.colors import Color


def get_names() -> List[str]:

    try:
        return list(dict.fromkeys([n[0] for n in db.session.query(Color.name).order_by(Color.name).all()]))
        # names = set([n[0] for n in session.query(Color.name).order_by(Color.name).all()])
    except:
        return []


def is_present(name: str) -> bool:
    name = name.lower().strip().title()

    try:
        return db.session.query(Color).filter(Color.name == name).all() != []
    except Exception as e:
        print('Exception: ', e)
        return None


def add(name: str):
    name = name.lower().strip().title()
    try:
        db.session.add(Color(name))
        db.session.commit()
        return name
    except:
        return None


def add_if_not_present(name: str) -> Optional[str]:
    if not is_present(name):
        return add(name)

    return name.lower().strip().title()


def get_id_from_name(name: str) -> Optional[int]:
    name = name.lower().strip().title()

    try:
        return db.session.query(Color.id).filter(Color.name == name).first()[0]
    except:
        return None
