import pytest


@pytest.fixture(scope="session")
def exemple_routes():
    routes = {
        "Tatooine": {"Dagobah": 6, "Hoth": 6},
        "Dagobah": {"Endor": 4, "Hoth": 1},
        "Hoth": {"Endor": 1},
    }
    return routes


@pytest.fixture(scope="session")
def exemple_bounty_hunters():
    return {("Hoth", 6), ("Hoth", 7), ("Hoth", 8)}
