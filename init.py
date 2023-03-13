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



def initialise(reservaties: List[Reservation], zones: List[Zone], voertuigen: List[Vehicle], interferences: List[List[bool]]) -> Tuple[List[Reservation], List[Zone]]:
    # problem: elke auto kan slechts op 1 reservatie staan?

    def sortNormal(reservatie: Reservation):
        return reservatie.id
    
    reservaties = sortReservaties(reservaties)

    used = []

    for res in reservaties:
        for posVeh in res.possibleVehicles:
            if posVeh not in used:
                used.append(posVeh)
                res.vehicle = voertuigen[posVeh]
                voertuigen[posVeh].zone = res.zone
                
                # for res2 in reservaties:
                #     if (res2.zone == res.zone) and (res2.vehicle is None) and not (interferences[res.id][res2.id]):
                #         res2.vehicle = voertuigen[posVeh]

    reservaties.sort(key=sortNormal)

    return reservaties, voertuigen