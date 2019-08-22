import unittest.mock

from sqlalchemy.orm import Session


def test_user_services_get_names_success(db_session_w_info):
    from travel_plan.services import user_services

    locations, users, colors = db_session_w_info

    actual_names = user_services.get_names()

    expected_names = sorted([u['name'] for u in users])

    assert actual_names == expected_names


def test_user_services_get_id_from_name_success(db_session_w_info):
    from travel_plan.services import user_services

    locations, users, colors = db_session_w_info

    number = 3

    expected_name = users[number]['name']

    actual_id = user_services.get_id_from_name(expected_name)

    assert actual_id == number + 1

# def test_get_all_no_search_terms_success(db_session_w_info):
#     from travel_plan.services import user_services
#
#     locations, users = db_session_w_info
#
#     all_users = user_services.get_users()
#
#     for u in all_users:
#         user = {'name': u.name, 'email': u.email, 'hashed_ssn': u.hashed_ssn}
#         assert user in users
#
#
# def test_get_all_w_1_search_term_success(db_session_w_info):
#     from travel_plan.services import user_services
#
#     locations, users = db_session_w_info
#
#     user = users[0]
#     us = user_services.get_users(name=user['name'])
#
#     assert len(us) == 1
#     assert us[0].name == user['name']
#     assert us[0].email == user['email']
#     assert us[0].hashed_ssn == user['hashed_ssn']
#
#
# def test_get_all_w_2_search_terms_success(db_session_w_info):
#     from travel_plan.services import user_services
#
#     locations, users = db_session_w_info
#
#     user = users[2]
#     us = user_services.get_users(name=user['name'], email=user['email'])
#
#     assert len(us) == 1
#     assert us[0].name == user['name']
#     assert us[0].email == user['email']
#     assert us[0].hashed_ssn == user['hashed_ssn']
#
#
# def test_get_all_w_2_search_terms_fail(db_session_w_info):
#     from travel_plan.services import user_services
#
#     locations, users = db_session_w_info
#
#     user = users[2]
#     us = user_services.get_users(name=user['name'], email='lkjiuhyguy')
#
#     assert len(us) == 0
