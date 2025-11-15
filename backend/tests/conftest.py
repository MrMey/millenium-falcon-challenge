import pytest
from pathlib import Path
from src.millenium_router.models import PlanetDay


BASE_DIR = Path(__file__).resolve()
ROUTES = [
    ("Tatooine", "Dagobah", 6),
    ("Tatooine", "Hoth", 6),
    ("Dagobah", "Endor", 4),
    ("Dagobah", "Hoth", 1),
    ("Hoth", "Endor", 1),
]


@pytest.fixture(scope="session")
def test_db_path():
    return BASE_DIR.parent / "universe.db"


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
        "src.millenium_router.core.get_neighbors_from_db",
        mock_get_neighbors_from_db,
    )


@pytest.fixture(scope="session")
def exemple_bounty_hunters():
    return {PlanetDay("Hoth", 6), PlanetDay("Hoth", 7), PlanetDay("Hoth", 8)}
