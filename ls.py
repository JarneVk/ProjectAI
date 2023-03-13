from typing import *
from DataStructure import *


class LocalSearch():

    def getPossibleAmountCars(reservation: Reservation):
            return len(reservation.possibleVehicles)

    def sortNormal(reservation: Reservation):
            return reservation.id

    def sortReservationsVehicles(self):
        # sorteer geinitialiseerde reservaties
        self.reservations.sort(key=LocalSearch.getPossibleAmountCars)

    def sortReservationsID(self):
        # sorteer geinitialiseerde reservaties
        self.reservations.sort(key=LocalSearch.sortNormal)

    def __init__(self, reservations: List[Reservation], zones: List[Zone], vehicles: List[Vehicle], interferences: List[List[bool]]) -> None:
        self.reservations = reservations
        self.zones = zones
        self.vehicles = vehicles
        self.interferences = interferences

    def initialise(self):
        self.sortReservationsVehicles()
        used = []

        for res in self.reservations:
            for posVeh in res.possibleVehicles:
                if posVeh not in used:
                    used.append(posVeh)
                    res.vehicle = self.vehicles[posVeh]
                    self.vehicles[posVeh].zone = res.zone

        self.sortReservationsID()


    def CheckAll(self) -> bool:

        for car in self.vehicles:
            # every car needs a zone
            if car.zone == None:
                print(f"auto {car.id} does not have a zone assigned")
                return False
            
        for res in self.reservations:

            # reservation is not filled in
            if res.vehicle == None:
                continue

            # two reservations for the same car intervene
            for indx, inter in enumerate(self.interferences[res.id]):
                if inter == True and res.vehicle == self.reservations[indx].vehicle:
                    print(f"overlapping reservations r1: {res.id} | r2: {self.reservations[indx].id}")
                    return False

        return True
    
    