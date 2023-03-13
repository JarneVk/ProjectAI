from DataStructure import *
from typing import *

def writeOutput(reservations: List[Reservation], zones: List[Zone], vehicles: List[Vehicle]):
    with open("output/test_1.csv", 'w') as file:
        for vehicle in vehicles:
            file.write(f"{vehicle.id};{vehicle.zone.id},\n")
        file.write("\n")
        for reservation in reservations:
            if reservation.vehiecel is None:
                continue
            else:
                file.write(f"{reservation.id};{reservation.vehiecel.id},\n")
        file.write("\n")
        for reservation in reservations:
            if reservation.vehiecel is None:
                file.write(f"{reservation.id},\n")