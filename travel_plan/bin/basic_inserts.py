import os
import sys

folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
data = os.path.join(folder, 'tests')
sys.path.insert(0, folder)
sys.path.insert(0, data)

import tests.conftest as conftest
try:
    import travel_plan.config as config
except:
    print('*'*10 + ' Did you create a config.py file from the config_example.py file? ' + '*'*10)
from travel_plan.models import db_session
from travel_plan.models.cars import Car
from travel_plan.models.colors import Color
from travel_plan.models.locations import Location
from travel_plan.models.users import User


def main():
    init_db()

    session = db_session.create_session()

    for n in conftest.cars:
        session.add(Car(**n))

    for n in conftest.users:
        session.add(User(**n))

    for n in conftest.locations:
        session.add(Location(**n))

    for n in conftest.colors:
        if not session.query(Color).filter(Color.name == n).all():
            session.add(Color(n))
            session.commit()

    session.commit()
    session.close()


def init_db():
    db_path = config.DB_FOLDER_PATH
    os.makedirs(db_path, exist_ok=True)
    db_file = os.path.abspath(os.path.join(db_path, config.DB_NAME))
    db_session.global_init(db_file)


if __name__ == '__main__':
    main()
