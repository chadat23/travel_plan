def test_department_services_get_id_from_name(app_w_db, departments):
    from travel_plan.department import department_services

    ids = [department_services.get_id_from_name(i['name']) for i in departments]

    for i, id in enumerate(ids):
        assert i + 1 == id


def test_department_services_get_id_from_name_w_nones(app_w_db):
    from travel_plan.department import department_services

    assert not department_services.get_id_from_name(None)
