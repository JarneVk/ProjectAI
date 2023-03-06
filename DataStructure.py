from dataclasses import dataclass


@dataclass
class Zone():
    id:int
    neighbours:list[int]

@dataclass
class Vehiecels():
    id:int
    zone:Zone = None

@dataclass
class Reservation():
    id:str
    zone:int
    day:int
    start:int
    restime:int
    possibleVehicels:list[int]
    vehiecel:Vehiecels = None
    p1:int
    p2:int

@dataclass
class Map():
    zones:list[Zone]



