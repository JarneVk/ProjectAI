from typing import *
from DataStructure import *
from copy import deepcopy


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
                # print(f"auto {car.id} does not have a zone assigned")
                return False
            
        for res in self.reservations:

            # reservation is not filled in
            if res.vehicle == None:
                continue

            # two reservations for the same car intervene
            for indx, inter in enumerate(self.interferences[res.id]):
                if inter == True and res.vehicle == self.reservations[indx].vehicle:
                    # print(f"overlapping reservations r1: {res.id} | r2: {self.reservations[indx].id}")
                    return False

        return True
    
    def checkNew(self, reservations: List[Reservation]) -> bool:
        for car in self.vehicles:
            if car.zone == None:
                print(f"auto {car.id} does not have a zone assigned")
                return False
            
        for res in reservations:
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
            elif res.vehicle.zone.id in res.zone.neighbours:
                total_cost += res.p2

        return total_cost
    
    # localSearch
    def carToZone(self, car: Vehicle, zone: Zone) -> bool:

        for res in self.reservations:
            if res.vehicle is not None:
                if res.vehicle.id == car.id:
                   res.vehicle = None

        assigned = False
        for reservation in self.reservations:
            if (reservation.zone.id == zone.id) and (reservation.vehicle is None):
                reservation.vehicle = car
                car.zone = zone
                assigned = True

            # also assign possible neigbours
            elif reservation.vehicle is None and zone.id in reservation.zone.neighbours:
                reservation.vehicle = car
                car.zone = zone
                assigned = True
                
        if not assigned:
            # print("not possible to assign vehicle to zone")
            None

    def switchCarToNeighbours(self, car: int) -> List[Reservation]:

        currentBestCost = self.calculateFullCosts()
        reservationsBest = deepcopy(self.reservations)
        vehiclesBest = deepcopy(self.vehicles)

        for z in car.zone.neighbours:
            self.carToZone(car, self.zones[z])
            cost = self.calculateFullCosts()
            # change is correct
            if cost < currentBestCost and self.checkAll():
                currentBestCost = cost
                reservationsBest = deepcopy(self.reservations)
                vehiclesBest = deepcopy(self.vehicles)
            # change is not correct
            else:
                self.reservations = deepcopy(reservationsBest)
                self.vehicles = deepcopy(vehiclesBest)
                
        print(self.checkAll())

    def writeOutput(self, filename: str):
        with open(filename, 'w') as file:
            file.write(f"{self.calculateFullCosts()}\n")
            file.write(f"+Vehicle assignments\n")

            for vehicle in self.vehicles:
                file.write(f"car{vehicle.id};z{vehicle.zone.id}\n")

            file.write("+Assigned requests\n")
            for reservation in self.reservations:
                if reservation.vehicle is None:
                    continue
                else:
                    file.write(f"req{reservation.id};car{reservation.vehicle.id}\n")

            file.write("+Unassigned requests\n")
            for reservation in self.reservations:
                if reservation.vehicle is None:
                    file.write(f"req{reservation.id}\n")