from typing import *
from DataStructure import *
from control import *
from cost import *

def carToZone(car: Vehicle, zone: Zone, reservations: List[Reservation]) -> bool:
    assigned = False
    for reservation in reservations:
        #check for own zone to minimise cost
        if reservation.zone.id == zone.id and reservation.vehiecel is None:
            reservation.vehiecel = car
            car.zone = zone.id
            assigned = True
        
        #also assign possible neigbours
        elif reservation.vehiecel is None and zone.id in reservation.zone.neighbours:
            reservation.vehiecel = car
            car.zone = zone.id
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


def LocalSearch():
    #take a random number, move the car with that id to a neighbour
    pass