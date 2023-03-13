from dataclasses import dataclass
from typing import *


@dataclass(slots=True)
class Zone():
    id:int
    neighbours:List[int]

@dataclass(slots=True)
class Vehicle():
    id:int
    zone:Zone = None

@dataclass(slots=True)
class Reservation():
    id:int
    zone:Zone
    day:int
    start:int
    restime:int
    possibleVehicles:List[int]
    p1:int
    p2:int
    vehicle:Vehicle = None

@dataclass(slots=True)
class Map():
    zones:List[Zone]



