from millenium_router.core import compute_odds


def test_compute_odds():
    assert compute_odds("a", "b").is_integer()