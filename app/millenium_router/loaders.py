import json
import sqlite3
import os
import logging
from collections import defaultdict
from pydantic import ValidationError
from .models import Empire, Falcon

logger = logging.getLogger(__name__)


def load_empire_data(empire_path) -> dict:
    with open(empire_path) as f:
        empire_data = Empire(**json.load(f))
    
    return empire_data
    

def load_falcon_data(falcon_path):
    with open(falcon_path) as f:
        falcon_data = Falcon(**json.load(f))
    
    base_dir = os.path.dirname(falcon_path)
    routes_path = os.path.join(base_dir, falcon_data.routes_db)

    if not os.path.exists(routes_path):
        raise FileNotFoundError(f"Could not find {falcon_data['routes_db']}")
    
    return falcon_data.autonomy, falcon_data.departure, falcon_data.arrival, routes_path


def load_universe_data(universe_path, autonomy, departure, arrival) -> dict:
    routes = defaultdict(lambda : defaultdict(int))

    with sqlite3.connect(universe_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT * from routes;""")
        
        departure_seen = False
        arrival_seen = False

        for leg_departure, leg_arrival, distance in cursor:
            if distance > autonomy:
                logger.debug('Do not load {leg_departure}:{leg_arrival} in {distance} days because exceeding autonomy={autonomy}')
                continue
            
            if departure == leg_departure:
                departure_seen = True
            
            if arrival == leg_arrival:
                arrival_seen = True
            
            routes[leg_departure][leg_arrival] = distance

        if not departure_seen:
            raise ValueError(f'departure {departure} not found in the universe data')

        if not arrival_seen:
            raise ValueError(f'departure {arrival} not found in the universe data')
    return routes