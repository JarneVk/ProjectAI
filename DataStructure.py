from dataclasses import dataclass


@dataclass
class Zone():
    id:int
    neighbours:list[int]

@dataclass
class Vehicle():
    id:int
    zone:Zone = None

@dataclass
class Reservation():
    id:str
    zone:int
    day:int
    start:int
    restime:int
    possibleVehicles:list[int]
    p1:int
    p2:int
    vehiecel:Vehicle = None

@dataclass
class Map():
    zones:list[Zone]



