from parser_1 import read_file
import pprint
from DataStructure import *
from typing import *

5
def sortReservaties(reservaties: List[Reservation]):

    def getPossibleAmountCars(reservatie: Reservation):
        return len(reservatie.possibleVehicles)

    # sorteer geinitialiseerde reservaties
    reservaties.sort(key=getPossibleAmountCars)
    return reservaties

def initialise(reservaties: List[Reservation], zones: List[Zone], voertuigen: List[Vehicle]) -> Tuple[List[Reservation], List[Zone]]:

    reservaties = sortReservaties(reservaties)

    used = []

    for res in reservaties:
        for posVeh in res.possibleVehicles:
            if posVeh not in used:
                used.append(posVeh)
                res.vehiecel = voertuigen[posVeh]
                voertuigen[posVeh].zone = zones[res.zone]

    return reservaties, voertuigen