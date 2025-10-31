import argparse
import logging

from app.millenium_router.loaders import load_empire_data, load_falcon_data, load_universe_data


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def find_paths(routes, departure, arrival, countdown, autonomy, bounty_hunters):
    queue = [((departure,), 0, autonomy, 0)]

    iterations = 0
    min_capture_attempts = 0
    best_path = None

    logger.debug(routes)

    while queue:
        if iterations > 10:
            break

        planets, day_no, fuel, capture_attempts = queue.pop(0)
        current_planet = planets[-1]

        if (current_planet, day_no) in bounty_hunters:
            capture_attempts += 1
        
        neighbors = routes[current_planet]

        for neighbor, distance in neighbors.items():
            if distance > fuel:
                continue

            if distance > countdown - day_no:
                continue

            if neighbor == arrival:
                logger.debug("Found a path %s when capture %i", planets, capture_attempts)
                if best_path is None or capture_attempts < min_capture_attempts:
                    min_capture_attempts = capture_attempts
                    best_path = tuple((*planets, neighbor))

                if capture_attempts == 0:
                    logger.debug("Found a safe path. No need to search more")
                    break

                continue
            
            if distance + day_no == countdown:
                continue
            
            logger.debug("will jump to %s in %i", neighbor, distance)
            queue.append((tuple((*planets, neighbor)), day_no + distance, fuel - distance, capture_attempts))
        
        queue.append((tuple((*planets, current_planet)), day_no + 1, autonomy, capture_attempts))
        logger.debug("will wait in %s", current_planet)

        iterations += 1

    return best_path, min_capture_attempts


def compute_odds(capture_attempts: int) -> int:
    if capture_attempts == 0:
        capture_chance = 0.0
    elif capture_attempts == 1:
        capture_chance = 0.1
    else:
        capture_chance = 0.1 + sum(9 ** (k-1) / 10 ** k for k in range(2, capture_attempts + 1))
    
    return int(100 * (1 - capture_chance))


def explore(falcon_path, empire_path) -> int:
    falcon = load_falcon_data(falcon_path)
    logger.debug(falcon)

    empire = load_empire_data(empire_path)
    logger.debug(empire.countdown)

    routes = load_universe_data(falcon_path, falcon.routes_db)
     
    path, capture_attempts = find_paths(
        routes,
        falcon.departure,
        falcon.arrival, 
        empire.countdown,
        falcon.autonomy,
        bounty_hunters=empire.bounty_hunters
    )

    odds = compute_odds(capture_attempts)
    print(odds)


def launch():
    parser = argparse.ArgumentParser()
    parser.add_argument('millenium_falcon_path', help="input json file containing the millenium falcon data")
    parser.add_argument('empire_path', help="input json file containing the empire data")

    args = parser.parse_args()
    print(explore(args.millenium_falcon_path, args.empire_path))


if __name__ == "__main__":
    launch()