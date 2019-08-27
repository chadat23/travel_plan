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
