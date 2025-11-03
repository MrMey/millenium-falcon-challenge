from backend.millenium_router.core import compute_odds, find_paths


def test_compute_odds():
    assert compute_odds(0) == 100
    assert compute_odds(1) == 90
    assert compute_odds(2) == 81
    


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
    assert best_path == (('Tatooine', 0), ('Hoth', 6), ('Hoth', 7), ('Endor', 8))
    assert capture_attempts == 0


def test_exemple_1(exemple_routes, exemple_bounty_hunters):
    best_path, capture_attempts = find_paths(
        exemple_routes, 
        "Tatooine", 
        "Endor", 
        countdown=7, 
        autonomy=6, 
        bounty_hunters=exemple_bounty_hunters)

    assert best_path == None
    assert capture_attempts == 0


def test_exemple_2(exemple_routes, exemple_bounty_hunters):
    best_path, capture_attempts = find_paths(
        exemple_routes, 
        "Tatooine", 
        "Endor", 
        countdown=8, 
        autonomy=6, 
        bounty_hunters=exemple_bounty_hunters)

    assert best_path == (('Tatooine', 0), ('Hoth', 6), ('Hoth', 7), ('Endor', 8))
    assert capture_attempts == 2


def test_exemple_3(exemple_routes, exemple_bounty_hunters):
    best_path, capture_attempts = find_paths(
        exemple_routes, 
        "Tatooine", 
        "Endor", 
        countdown=9, 
        autonomy=6, 
        bounty_hunters=exemple_bounty_hunters)
    assert best_path == (('Tatooine', 0), ('Dagobah', 6), ('Dagobah', 7), ('Hoth', 8), ('Endor', 9))
    assert capture_attempts == 1


def test_exemple_4(exemple_routes, exemple_bounty_hunters):
    best_path, capture_attempts = find_paths(
        exemple_routes, 
        "Tatooine", 
        "Endor", 
        countdown=10, 
        autonomy=6, 
        bounty_hunters=exemple_bounty_hunters)
    assert best_path == (('Tatooine', 0), ('Dagobah', 6), ('Dagobah', 7), ('Dagobah', 8), ('Hoth', 9), ('Endor', 10))
    assert capture_attempts == 0