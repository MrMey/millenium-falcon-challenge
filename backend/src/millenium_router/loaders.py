import json
import os
import logging
from typing import Tuple, List
from .models import Falcon, PlanetDay, Empire


logger = logging.getLogger(__name__)


def load_empire_data(empire_input: dict) -> Tuple[int, List[PlanetDay]]:
    empire_data = Empire(**empire_input)

    bounty_hunters = set(
        PlanetDay(el.planet, el.day) for el in empire_data.bounty_hunters
    )
    return empire_data.countdown, bounty_hunters


def load_falcon_data(falcon_path):
    with open(falcon_path) as f:
        falcon_data = Falcon(**json.load(f))

    base_dir = os.path.dirname(falcon_path)
    routes_path = os.path.join(base_dir, falcon_data.routes_db)

    if not os.path.exists(routes_path):
        raise FileNotFoundError(f"Could not find {falcon_data['routes_db']}")

    return falcon_data.autonomy, falcon_data.departure, falcon_data.arrival, routes_path
