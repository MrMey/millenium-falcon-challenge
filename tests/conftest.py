import pytest


ROUTES = [
    ("Tatooine", "Dagobah", 6),
    ("Tatooine", "Hoth", 6),
    ("Dagobah", "Endor", 4),
    ("Dagobah", "Hoth", 1),
    ("Hoth", "Endor", 1),
]


def mock_get_neighbors_from_db(cursor, origin, max_distance):
    results = [
        (leg_destination, leg_travel_time)
        for (leg_origin, leg_destination, leg_travel_time) in ROUTES
        if leg_origin == origin and leg_travel_time <= max_distance
    ]
    return results


@pytest.fixture
def mocked_routes(monkeypatch):
    monkeypatch.setattr(
        "backend.millenium_router.core.get_neighbors_from_db",
        mock_get_neighbors_from_db,
    )


@pytest.fixture(scope="session")
def exemple_bounty_hunters():
    return {("Hoth", 6), ("Hoth", 7), ("Hoth", 8)}
