from app.millenium_router.core import compute_odds, find_paths


def test_compute_odds():
    assert compute_odds(0) == 100
    assert compute_odds(1) == 90


def test_countdown_too_low():
    routes = {
        'Tatooine': {'Dagobah': 6, 'Hoth': 6}, 
        'Dagobah': {'Endor': 4, 'Hoth': 1},
         'Hoth': {'Endor': 1}
    }
    best_path, capture_attempts = find_paths(
        routes,
        departure='Tatooine',
        arrival='Endor',
        countdown=5,
        autonomy=6,
        bounty_hunters=set()
    )
    assert best_path is None
    assert capture_attempts == 0

def test_safe_path():
    routes = {
        'Tatooine': {'Dagobah': 6, 'Hoth': 6}, 
        'Dagobah': {'Endor': 4, 'Hoth': 1},
         'Hoth': {'Endor': 1}
    }

    best_path, capture_attempts = find_paths(
        routes,
        departure='Tatooine',
        arrival='Endor',
        countdown=8,
        autonomy=6,
        bounty_hunters=set()
    )
    assert best_path == ('Tatooine', 'Hoth', 'Hoth', 'Endor')
    assert capture_attempts == 0

