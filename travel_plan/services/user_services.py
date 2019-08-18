from typing import List, Optional

from sqlalchemy.orm import Session

from travel_plan.models import db_session
from travel_plan.models.users import User


def get_users(name: str = '%', email: str = '%', hashed_ssn: str = '%') -> List[User]:
    '''
    Get all the Users where ANY of the properties match.

    :param name:
    :param email:
    :param hashed_ssn:
    :return:
    '''
    from sqlalchemy import and_

    session: Session = db_session.create_session()

    try:

        if name == '%' and email == '%' and hashed_ssn == '%':
            users = session.query(User).all()
        else:
            users = list(session.query(User).filter(and_(User.name.like(name),
                                                    User.email.like(email),
                                                    User.hashed_ssn.like(hashed_ssn))))
    except:
        users = []
    finally:
        session.close()

    return users


def add_user(name: str, email: str, hashed_ssn: str, update_existing: bool = True) -> Optional[User]:
    session: Session = db_session.create_session()
    try:
        users = get_users(name, email, hashed_ssn)
        if not users:
            user = User(name=name, email=email, hashed_ssn=hashed_ssn)
            session.add(user)
        elif len(users) > 1:
            return None
        else:
            if update_existing:
                pass
            else:
                pass
    except:
        users = []
    finally:
        session.close()

    return users
