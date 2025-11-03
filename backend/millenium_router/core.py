import logging


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def find_paths(routes, departure, arrival, countdown, autonomy, bounty_hunters):
    queue = [(((departure, 0),), autonomy, 0)]

    print(routes)
    iterations = 0

    min_capture_attempts = 0
    best_path = None
    min_days = None

    while queue:
        planets, fuel, capture_attempts = queue.pop(0)
        current_planet, day_no = planets[-1]

        if (current_planet, day_no) in bounty_hunters:
            capture_attempts += 1
        
        neighbors = routes[current_planet]

        for neighbor, distance in neighbors.items():
            if distance > fuel:
                continue

            if distance > countdown - day_no:
                continue

            if neighbor == arrival:
                if (
                        best_path is None 
                        or capture_attempts < min_capture_attempts
                        or (min_days < (day_no + distance) and capture_attempts == min_capture_attempts)
                    ):
                    min_capture_attempts = capture_attempts
                    min_days = day_no + distance
                    best_path = ((*planets, (neighbor, day_no + distance)))

                if capture_attempts == 0:
                    logger.debug("Found a safe path. No need to search more")
                    return best_path, min_capture_attempts

                continue
            
            if distance + day_no == countdown:
                continue
            
            logger.debug("will jump to %s in %i day(s)", neighbor, distance)
            queue.append(
                (
                    (*planets, (neighbor, day_no + distance)), 
                    fuel - distance, capture_attempts
                )
            )
        
        if day_no + 1 <= countdown:
            queue.append((((*planets, (current_planet, day_no + 1))), autonomy, capture_attempts))
            logger.debug("will wait in %s", current_planet)

        iterations += 1

    return best_path, min_capture_attempts


def compute_odds(capture_attempts: int) -> int:
    """
    we can factorize / 10 in 
        1 / 10 + 9 ** 1 / 10**2 + 9**2 / 10 ** 3
    to get the geometrical sum of reason x = 0.9
        (1 + 0.9 + 0.9**2 + ...+ 0.9**(n-1))    / 10
    whose sums is:
        (1 - x**n) / (1 - x )                   / 10
    which ends up simply:
        0.9**n
    """
    return int(0.9**capture_attempts * 100)


def find_best_path_and_odds(routes, departure, arrival, countdown, autonomy, bounty_hunters) -> int:
    best_path, capture_attempts = find_paths(routes, departure, arrival, countdown, autonomy, bounty_hunters)

    if best_path is None:
        odds = 0
        logger.debug(f"Found no path with odds={odds}")
    else:
        odds = compute_odds(capture_attempts)
        logger.debug(f"Found this path {best_path} with capture_attemps={capture_attempts} and odds={odds}")

    return odds