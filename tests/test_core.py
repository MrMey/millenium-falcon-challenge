from backend.millenium_router.core import compute_odds, find_paths


def test_compute_odds():
    assert compute_odds(0) == 100
    assert compute_odds(1) == 90
    assert compute_odds(2) == 81
    assert compute_odds(3) == 73


def test_countdown_too_low(mocked_routes):
    best_path, capture_attempts = find_paths(
        None,  # fake_cursor
        departure="Tatooine",
        arrival="Endor",
        countdown=5,
        autonomy=6,
        bounty_hunters=set(),
    )
    assert best_path is None
    assert capture_attempts == 0


def test_safe_path(mocked_routes):
    best_path, capture_attempts = find_paths(
        None,  # fake_cursor
        departure="Tatooine",
        arrival="Endor",
        countdown=8,
        autonomy=6,
        bounty_hunters=set(),
    )
    assert best_path == (("Tatooine", 0), ("Hoth", 6), ("Hoth", 7), ("Endor", 8))
    assert capture_attempts == 0


def test_exemple_1(mocked_routes, exemple_bounty_hunters):
    best_path, capture_attempts = find_paths(
        None,  # fake_cursor
        "Tatooine",
        "Endor",
        countdown=7,
        autonomy=6,
        bounty_hunters=exemple_bounty_hunters,
    )

    assert best_path == None
    assert capture_attempts == 0


def test_exemple_2(mocked_routes, exemple_bounty_hunters):
    best_path, capture_attempts = find_paths(
        None,  # fake_cursor
        "Tatooine",
        "Endor",
        countdown=8,
        autonomy=6,
        bounty_hunters=exemple_bounty_hunters,
    )

    assert best_path == (("Tatooine", 0), ("Hoth", 6), ("Hoth", 7), ("Endor", 8))
    assert capture_attempts == 2


def test_exemple_3(mocked_routes, exemple_bounty_hunters):
    best_path, capture_attempts = find_paths(
        None,  # fake_cursor
        "Tatooine",
        "Endor",
        countdown=9,
        autonomy=6,
        bounty_hunters=exemple_bounty_hunters,
    )
    assert best_path == (
        ("Tatooine", 0),
        ("Dagobah", 6),
        ("Dagobah", 7),
        ("Hoth", 8),
        ("Endor", 9),
    )
    assert capture_attempts == 1


def test_exemple_4(mocked_routes, exemple_bounty_hunters):
    best_path, capture_attempts = find_paths(
        None,  # fake_cursor
        "Tatooine",
        "Endor",
        countdown=10,
        autonomy=6,
        bounty_hunters=exemple_bounty_hunters,
    )
    assert best_path == (
        ("Tatooine", 0),
        ("Dagobah", 6),
        ("Dagobah", 7),
        ("Dagobah", 8),
        ("Hoth", 9),
        ("Endor", 10),
    )
    assert capture_attempts == 0
