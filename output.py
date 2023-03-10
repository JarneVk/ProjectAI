from DataStructure import *
from typing import *

def writeOutput(filename: str,reservations: List[Reservation], zones: List[Zone], vehicles: List[Vehicle], cost: int):
    with open(filename, 'w') as file:
        file.write(f"{cost}\n")
        file.write(f"+Vehicle assignments\n")

        for vehicle in vehicles:
            file.write(f"car{vehicle.id};z{vehicle.zone.id}\n")

        file.write("+Assigned requests\n")
        for reservation in reservations:
            if reservation.vehicle is None:
                continue
            else:
                file.write(f"req{reservation.id};car{reservation.vehicle.id}\n")

        file.write("+Unassigned requests\n")
        for reservation in reservations:
            if reservation.vehicle is None:
                file.write(f"req{reservation.id}\n")