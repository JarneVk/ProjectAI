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
        self.reservations: List[Reservation] = reservations
        self.zones: List[Zone] = zones
        self.vehicles: List[Vehicle] = vehicles
        self.interferences: List[List[bool]] = interferences


    # Initialisatie
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

    # control
    def checkAll(self) -> bool:

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
    
    # cost
    def calculateFullCosts(self) -> int:

        total_cost = 0
        for res in self.reservations:

            # res not assigned
            if res.vehicle == None:
                total_cost += res.p1

            # res assigned car in own zone
            elif res.vehicle.zone == res.zone:
                total_cost += 0

            # res assigned in car in neighbouring zone 
            elif res.vehicle.zone in res.zone.neighbours:
                total_cost += res.p2

        return total_cost
    
    # localSearch
    def carToZone(self, car: Vehicle, zone: Zone) -> bool:
        assigned = False
        for reservation in self.reservations:
            if (reservation.zone.id == zone.id) and (reservation.vehicle is None):
                reservation.vehicle = car
                car.zone = zone
                assigned = True
                
        if not assigned:
            print("not possible to assign vehicle to zone")

    def switchCarToNeighbours(self, car: Vehicle) -> List[Reservation]:

        currentBestCost = self.calculateFullCosts()
        reservationsBest = self.reservations

        for z in car.zone.neighbours:
            self.carToZone(car, self.zones[z])
            cost = self.calculateFullCosts()
            if cost < currentBestCost and self.checkAll():
                currentBestCost = cost
                reservationsBest = self.reservations
            else:
                self.reservations = reservationsBest
                
        print(self.checkAll())