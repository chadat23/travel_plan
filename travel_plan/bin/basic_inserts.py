import os
# import sys
#
# folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
# data = os.path.join(folder, 'tests')
# sys.path.insert(0, folder)
# sys.path.insert(0, data)


import tests.conftest as conftest
from travel_plan import create_app


def main():
    app = create_app()

    from travel_plan import db
    from travel_plan.models.cars import Car
    from travel_plan.models.colors import Color
    from travel_plan.models.locations import Location
    from travel_plan.models.users import User

    # with app.app_context():
    for n in conftest._cars:
        db.session.add(Car(**n))

    for n in conftest._users:
        db.session.add(User(**n))

    for n in conftest._locations:
        db.session.add(Location(**n))

    for n in conftest._colors:
        if not db.session.query(Color).filter(Color.name == n).all():
            db.session.add(Color(n))
            db.session.commit()

    db.session.commit()


if __name__ == '__main__':
    main()
