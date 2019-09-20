from typing import List, Optional

from flask_sqlalchemy.orm import Session

from travel_plan.models import db_session
from travel_plan.models.travel_file import TravelFile


def is_present(name: str) -> bool:
    name = name.strip()

    session: Session = db_session.create_session()

    try:
        return session.query(TravelFile).filter(TravelFile.name == name).all()
    except:
        return None
    finally:
        session.close()
