from app.millenium_router.core import compute_odds


def test_compute_odds():
    assert compute_odds(0) == 100
    assert compute_odds(1) == 90
    