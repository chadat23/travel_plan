import unittest.mock

from sqlalchemy.orm import Session


def test_user_services_get_users_success(db_session_w_info):
    from travel_plan.services import user_services

    locations, users, colors, cars = db_session_w_info

    actual_users = user_services.get_users()

    never_ran = True
    for u in users:
        if u['name'] == actual_users[0].name:
            assert u['email'] == actual_users[0].email
            assert u['cell_number'] == actual_users[0].cell_number
            never_ran = False
            break
    assert not never_ran
    assert len(actual_users) == len(users)


def test_user_services_get_names_success(db_session_w_info):
    from travel_plan.services import user_services

    locations, users, colors, cars = db_session_w_info

    actual_names = user_services.get_names()

    expected_names = sorted([u['name'] for u in users])

    assert actual_names == expected_names


def test_user_services_get_id_from_name_success(db_session_w_info):
    from travel_plan.services import user_services

    locations, users, colors, cars = db_session_w_info

    number = 3

    expected_name = users[number]['name']

    actual_id = user_services.get_id_from_name(expected_name)

    assert actual_id == number + 1


def test_user_services_get_user_from_name_success(db_session_w_info):
    from travel_plan.models.users import User
    from travel_plan.services import user_services

    locations, users, colors, cars = db_session_w_info

    number = 3

    expected_user = users[number]

    actual_user = user_services.get_user_from_name(expected_user['name'])

    assert isinstance(actual_user, User)
    assert actual_user.name == expected_user['name']
    assert actual_user.email == expected_user['email']
    assert actual_user.cell_number == expected_user['cell_number']


def test_user_services_get_user_from_email_success(db_session_w_info):
    from travel_plan.models.users import User
    from travel_plan.services import user_services

    locations, users, colors, cars = db_session_w_info

    number = 3

    expected_user = users[number]

    actual_user = user_services.get_user_from_email(expected_user['email'])

    assert isinstance(actual_user, User)
    assert actual_user.name == expected_user['name']
    assert actual_user.email == expected_user['email']
    assert actual_user.cell_number == expected_user['cell_number']


def test_user_services_create_user_success(db_session_w_info):
    from travel_plan.models.users import User
    from travel_plan.services import user_services

    locations, users, colors, cars = db_session_w_info

    name = 'Bob'
    email = 'bob@email.com'
    work = '555-123-4567'
    home = '555-223-4567'
    cell = '555-323-4567'
    department = "Wilderness"
    active = False

    actual_user = user_services.create_user(name, email, work, home, cell, department, active)

    assert isinstance(actual_user, User)
    assert actual_user.name == name
    assert actual_user.email == email
    assert actual_user.cell_number == cell
    assert not actual_user.active


def test_user_services_update_user_success(db_session_w_info):
    from travel_plan.models.users import User
    from travel_plan.services import user_services

    locations, users, colors, cars = db_session_w_info

    number = 2
    retreaved_user = user_services.get_user_from_name(users[number]['name'])

    name = 'Bob'
    email = 'bob@email.com'
    work = '555-123-4567'
    home = '555-223-4567'
    cell = '555-323-4567'
    active = False

    actual_user = user_services.update_user(retreaved_user.id, active,
                                            name=name, email=email,
                                            work_number=work, home_number=home, cell_number=cell)

    assert isinstance(actual_user, User)
    assert actual_user.name == name
    assert actual_user.email == email
    assert actual_user.cell_number == cell
    assert not actual_user.active

    actual_user = user_services.get_user_from_name(actual_user.name)

    assert isinstance(actual_user, User)
    assert actual_user.name == name
    assert actual_user.email == email
    assert actual_user.cell_number == cell
    assert not actual_user.active
