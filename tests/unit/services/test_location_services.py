from sqlalchemy.orm import Session


def test_location_services_get_all_success(db_session_w_info):
    from travel_plan.services import location_services

    locations, users, colors, cars = db_session_w_info

    locs = location_services.get_all()

    for loc in locs:
        location = {'name': loc.name, 'latitude': loc.latitude, 'longitude': loc.longitude}
        assert location in locations


def test_location_services_get_names_success(db_session_w_info):
    from travel_plan.services import location_services

    locations, users, colors, cars = db_session_w_info

    actual_locacitons = location_services.get_names()

    expected_locations = sorted([n['name'] for n in locations])

    assert expected_locations == actual_locacitons


def test_location_services_get_id_from_name_success(db_session_w_info):
    from travel_plan.services import location_services

    locations, users, colors, cars = db_session_w_info

    actual_locaction = location_services.get_id_from_name(locations[1]['name'])

    expected_location = 2

    assert expected_location == actual_locaction


def test_location_services_add_location_returns_location(db_session_wo_info: Session):
    from travel_plan.models.locations import Location
    from travel_plan.services.location_services import add_location

    name = "LYV"
    latitude = 37.733023
    longitude = -119.514508

    location = add_location(name, latitude, longitude)

    assert isinstance(location, Location)
    assert name == location.name
    assert latitude == location.latitude
    assert longitude == location.longitude


def test_location_services_get_location_from_name_success(db_session_w_info):
    from travel_plan.models.locations import Location
    from travel_plan.services import location_services

    locations, users, colors, cars = db_session_w_info

    for location in locations:
        loc = location_services.get_location_from_name(location['name'])
        assert isinstance(loc, Location)
        assert loc.name == location['name']
        assert loc.latitude == location['latitude']
        assert loc.longitude == location['longitude']
