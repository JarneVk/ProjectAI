from parser_1 import read_file
import pprint
from DataStructure import *
from typing import *

def getPossibleAmountCars(reservation: Reservation):
        return len(reservation.possibleVehicles)

def sortNormal(reservation: Reservation):
        return reservation.id

def sortReservations(reservation: List[Reservation]):
    # sorteer geinitialiseerde reservaties
    reservation.sort(key=getPossibleAmountCars)
    return reservation



def initialise(reservations: List[Reservation], zones: List[Zone], vehicles: List[Vehicle], interferences: List[List[bool]]) -> Tuple[List[Reservation], List[Zone]]:
    
    # sort reservations from least cars possible to most
    reservations: List[Reservation] = sortReservations(reservations)

    used = []

    for res in reservations:
        for posVeh in res.possibleVehicles:
            if posVeh not in used:
                used.append(posVeh)
                res.vehicle = vehicles[posVeh]
                vehicles[posVeh].zone = res.zone

    reservations.sort(key=sortNormal)

    return reservations, vehicles