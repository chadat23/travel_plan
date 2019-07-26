import os
import travel_plan
import travel_plan.sql_models.db_session as db_session
from travel_plan.sql_models.locations import Location
from travel_plan.sql_models.user import User


def main():
    print('What do you want to do? Pick a number.')
    print(' 1: insert locations')
    print(' 2: insert users')
    choice = input()

    init_db()
    if choice == '1':
        insert_locations()
    elif choice == '2':
        insert_users()


def insert_users():
    session = db_session.create_session()

    u = User()
    u.name = 'Jane Dow'
    u.email = 'jane_dow@nps.gov'

    session.add(u)

    u = User()
    u.name = 'John Dow'
    u.email = 'john_dow@nps.gov'

    session.add(u)

    u = User()
    u.name = 'Darth Vader'
    u.email = 'darth_vader@nps.gov'

    session.add(u)

    u = User()
    u.name = 'Roger Rabbit'
    u.email = 'roger_rabbit@nps.gov'

    session.add(u)

    u = User()
    u.name = 'Rocky Balboa'
    u.email = 'rocky_balboa@nps.gov'

    session.add(u)
    session.commit()


def insert_locations():
    # https://www.latlong.net/
    session = db_session.create_session()

    loc = Location()
    loc.name = "Ten Lakes TH"
    loc.latitude = 37.852321
    loc.longitude = -119.575861

    session.add(loc)

    loc = Location()
    loc.name = "Ten Lakes Basin"
    loc.latitude = 37.899158
    loc.longitude = -119.522609

    session.add(loc)

    loc = Location()
    loc.name = "May Lake TH"
    loc.latitude = 37.832687
    loc.longitude = -119.490761

    session.add(loc)

    loc = Location()
    loc.name = "May Lake HSC"
    loc.latitude = 37.844617
    loc.longitude = -119.491018

    session.add(loc)
    session.commit()


def init_db():
    top_folder = os.path.dirname(__file__)
    rel_file = os.path.join('..', 'db', 'existing.sqlite')
    db_file = os.path.abspath(os.path.join(top_folder, rel_file))
    db_session.global_init(db_file)


if __name__ == '__main__':
    main()
