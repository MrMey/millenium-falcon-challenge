from typing import List
from pydantic import BaseModel


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
