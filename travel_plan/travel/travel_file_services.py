from travel_plan import db
from travel_plan.travel.travel_file import TravelFile


def is_present(name: str) -> bool:
    name = name.strip()

    try:
        return db.session.query(TravelFile).filter(TravelFile.name == name).all()
    except:
        return None
