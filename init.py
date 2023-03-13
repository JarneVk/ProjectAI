from parser_1 import read_file
import pprint
from DataStructure import *
from typing import *


def sortReservaties(reservaties: List[Reservation]):

    def getPossibleAmountCars(reservatie: Reservation):
        return len(reservatie.possibleVehicles)

    # sorteer geinitialiseerde reservaties
    reservaties.sort(key=getPossibleAmountCars)
    return reservaties

def initialise(reservaties: List[Reservation], zones: List[Zone], voertuigen: List[Vehicle]) -> Tuple[List[Reservation], List[Zone]]:
    # problem: elke auto kan slechts op 1 reservatie staan?

    reservaties = sortReservaties(reservaties)

    used = []

    for res in reservaties:
        for posVeh in res.possibleVehicles:
            if posVeh not in used:
                used.append(posVeh)
                res.vehiecel = voertuigen[posVeh]
                voertuigen[posVeh].zone = zones[res.zone]
                
                for res2 in reservaties:
                    if res2.zone.id == res.zone.id and res2.vehiecel is None:
                        res2.vehiecel = voertuigen[posVeh]


    return reservaties, voertuigen