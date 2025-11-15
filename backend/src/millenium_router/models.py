from typing import List, NamedTuple
from pydantic import BaseModel


class PlanetDay(NamedTuple):
    planet: str
    day_num: int

    def __repr__(self):
        return f"{self.planet}[{self.day_num}]"


class BountyHunterPosition(BaseModel):
    planet: str
    day: int


class Empire(BaseModel):
    countdown: int
    bounty_hunters: List[BountyHunterPosition]


class Falcon(BaseModel):
    autonomy: int
    departure: str
    arrival: str
    routes_db: str
