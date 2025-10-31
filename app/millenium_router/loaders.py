import json
import sqlite3
import os
from collections import defaultdict
from dataclasses import dataclass

@dataclass(frozen=True)
class FalconData:
    autonomy: int
    departure: str
    arrival: str
    routes_db: str


@dataclass(frozen=True)
class EmpireData:
    countdown: int
    bounty_hunters: set


def load_falcon_data(falcon_path) -> FalconData:
    with open(falcon_path) as f:
        falcon_data = json.load(f)
    
    return FalconData(
        falcon_data['autonomy'],
        falcon_data['departure'],
        falcon_data['arrival'],
        falcon_data['routes_db']
    )


def load_empire_data(empire_path) -> EmpireData:
    with open(empire_path) as f:
        empire_data = json.load(f)
    
    if not isinstance(empire_data['countdown'], int):
        raise ValueError('countdown should be a int')
    
    bounty_hunters = set()
    for bounty_hunter_position in empire_data['bounty_hunters']:
        if len(bounty_hunter_position) != 2:
            raise ValueError

        bounty_hunters.add((bounty_hunter_position['planet'], bounty_hunter_position['day']))

    return EmpireData(
        empire_data['countdown'],
        bounty_hunters
    )


def load_universe_data(falcon_path, db_relative_path) -> dict:
    routes = defaultdict(lambda : defaultdict(int))

    path = os.path.join(os.path.dirname(falcon_path), db_relative_path)
    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT * from routes;""")
        
        for departure, arrival, distance in cursor:
            routes[departure][arrival] = distance
    
    return routes