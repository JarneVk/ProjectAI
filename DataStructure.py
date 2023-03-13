from dataclasses import dataclass


@dataclass(slots=True)
class Zone():
    id:int
    neighbours:list[int]

@dataclass(slots=True)
class Vehicle():
    id:int
    zone:Zone = None

@dataclass(slots=True)
class Reservation():
    id:str
    zone:Zone
    day:int
    start:int
    restime:int
    possibleVehicles:list[int]
    p1:int
    p2:int
    vehiecel:Vehicle = None

@dataclass(slots=True)
class Map():
    zones:list[Zone]



