import DataStructure
from typing import *

def CalculateCosts(reservatorions: List[DataStructure.Reservation], zones: List[DataStructure.Zone]) -> int:

    total_cost = 0
    for res in reservatorions:

        # res not assigned
        if res.vehiecel == None:
            total_cost += res.p2

        # res assigned car in own zone
        elif res.vehiecel.zone.id == res.zone:
            total_cost += 0

        # res assigned in car in neighbouring zone 
        elif res.vehiecel in zones[res.zone].neighbours:
            total_cost += res.p1

    return total_cost
