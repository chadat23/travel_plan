def test_users_equal_success():
    from travel_plan.models.travel_file import TravelFile
    from travel_plan.models.travel_user_units import TravelUserUnit
    from travel_plan.models.users import User

    name = 'Bob'
    email = 'bob@email.com'
    work = '555-123-4567'
    home = '555-223-4567'
    cell = '555-323-4567'
    department = 'Wilderness'
    active = False

    user1 = User(name, email, work, home, cell, department, active)
    user2 = User(name, email, work, home, cell, department, active)

    assert user1 == user2


def test_users_equal_fail_success():
    from travel_plan.models.travel_file import TravelFile
    from travel_plan.models.travel_user_units import TravelUserUnit
    from travel_plan.models.users import User

    name = 'Bob'
    email = 'bob@email.com'
    work = '555-123-4567'
    home = '555-223-4567'
    cell = '555-323-4567'
    department = 'Wilderness'
    active = False

    user1 = User(name, email, work, home, cell, department, active)
    user2 = User('Bob2', email, work, home, cell, department, active)

    assert user1 != user2
