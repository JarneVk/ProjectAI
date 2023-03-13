from typing import *
from DataStructure import *
from control import *
from cost import *

def carToZone(car: Vehicle, zone: Zone, reservations: List[Reservation]) -> bool:
    assigned = False
    for reservation in reservations:
        if reservation.zone.id == zone.id and reservation.vehicle is None:
            reservation.vehicle = car
            car.zone = zone
            assigned = True
            
    if not assigned:
        print("not possible to assign vehicle to zone")
        return reservations
    
    return reservations

def switchCarToNeighbours(car: Vehicle, reservations: List[Reservation], zones: List[Zone], costFunction: Callable[[List[Reservation], List[Zone]], int]) -> List[Reservation]:

    currentCost = CalculateCosts(reservations, zones)
    reservations_or = reservations

    for z in car.zone.neighbours:
        reservations = carToZone(car, zones[z], reservations)
        if currentCost <= CalculateCosts(reservations, zones):
            reservations = reservations_or
    return reservations

def resToOtherVehicle():
    None