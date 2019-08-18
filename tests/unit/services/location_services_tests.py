import unittest.mock

from sqlalchemy.orm import Session


def test_add_location_returns_location(db_test_session: Session):
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


def test_get_location_success(db_session_w_info: Session):
    from travel_plan.models.locations import Location
    from travel_plan.services.location_services import get_location

    name = "LYV"
    latitude = 37.733023
    longitude = -119.514508

    location = get_location(name)

    assert isinstance(location, Location)
    assert name == location.name
    assert latitude == location.latitude
    assert longitude == location.longitude
