from typing import List, Optional

from travel_plan import db
from travel_plan.color.colors import Color


def get_names() -> Optional[List[str]]:
    """
    Gets the names of all the available colors.

    :return: a list of strings of the color names
    :rtype: Optional[List[str]]
    """

    try:
        return list(dict.fromkeys([n[0] for n in db.session.query(Color.name).order_by(Color.name).all()]))
    except:
        return []


def is_present(name: str) -> bool:
    """
    Checks if a color is present in the database.

    :param name: the name of the color to be checked
    :type name: str
    :return: True of the color is present, otherwise False
    :rtype: bool or None
    """

    try:
        name = name.lower().strip().title()
        return db.session.query(Color).filter(Color.name == name).all() != []
    except Exception as e:
        return None


def add(name: str) -> Optional[str]:
    """
    Save the color name to the database.

    :param name: the name of the color to be added to the database
    :return: the color name as a str if it was successful, otherwise None
    :rtype: Optional[str]
    """

    try:
        name = name.lower().strip().title()
        db.session.add(Color(name))
        db.session.commit()
        return name
    except:
        return None


def add_if_not_present(name: str) -> Optional[str]:
    """
    Save the color to the db if it isn't present.

    A convenience function combining is_present and add.

    :param name: the name of the color to be checked and maybe added.
    :return: the color name formatted to title format if apready 
    present or added, or None if there was a problem
    :rtype: Optional[str]
    """
    if not name:
        return None

    if not is_present(name):
        return add(name)

    return name.lower().strip().title()


def get_id_by_name(name: str) -> Optional[int]:
    """
    Get the id of the color with the supplied name.

    :param name: a str of the color name
    :return: int if successful, otherwise None
    :rtype: Optional[int]
    """

    try:
        name = name.lower().strip().title()
        return db.session.query(Color.id).filter(Color.name == name).first()[0]
    except:
        return None
