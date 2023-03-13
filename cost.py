import DataStructure
from typing import *

def CalculateCosts(reservatorions: List[DataStructure.Reservation], zones: List[DataStructure.Zone]) -> int:

    total_cost = 0
    for res in reservatorions:

        # res not assigned
        if res.vehicle == None:
            total_cost += res.p1

        # res assigned car in own zone
        elif res.vehicle.zone.id == res.zone:
            total_cost += 0

        # res assigned in car in neighbouring zone 
        elif res.vehicle in res.zone.neighbours:
            total_cost += res.p2

    return total_cost