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

    def doesInterfere(res1: Reservation, res2: Reservation) -> bool:
    # interference if start AND/OR end of second is in duration of first reservation
    # returns True if both reservations interfere with each other
    # returns False if not

        if res1.day != res2.day:
            return False

        start_1 = res1.start
        end_1 = res1.start + res1.restime
        start_2 = res2.start
        end_2 = res2.start + res2.restime

        if start_1 <= start_2 and start_2 <= end_1:
            return True
        elif start_1 <= end_2 and end_2 <= end_1:
            return True
        elif start_1 <= end_2 and start_2 <= end_1:
            return True
        return False
    
    def doesListInterfere(res1: Reservation, resList: List[Reservation]) -> bool:
    # check interference with list of Reservations

        for res2 in resList:
            if LocalSearch.doesInterfere(res1, res2):
                return True
        
        return False
    
    def vehiclePossible(vehicle: Vehicle, res: Reservation) -> bool:
        return res.zone.id == vehicle.zone.id and res.vehicle is None and vehicle.id in res.possibleVehicles


    def __init__(self, reservations: List[Reservation], zones: List[Zone], vehicles: List[Vehicle], interferences: List[List[bool]], debug: bool = False) -> None:
        self.reservations: List[Reservation] = reservations
        self.zones: List[Zone] = zones
        self.vehicles: List[Vehicle] = vehicles
        self.interferences: List[List[bool]] = interferences
        self.debug = debug


    # Initialisatie
    def initialise(self):
        self.sortReservationsVehicles()
        used = []
        res_per_veh = [[] for _ in range(len(self.vehicles))]

        for res in self.reservations:
            for posVeh in res.possibleVehicles:
                if posVeh not in used:
                    used.append(posVeh)
                    res.vehicle = self.vehicles[posVeh]
                    self.vehicles[posVeh].zone = res.zone
                    res_per_veh[posVeh].append(res.id)

        self.sortReservationsID()

        # loop for every vehicle through the list of reservations sorted by zone and look if you can add more than 1
        for vehicle in self.vehicles:
            for res in self.reservations:
                if LocalSearch.vehiclePossible(vehicle, res):
                    if not LocalSearch.doesListInterfere(res, [self.reservations[i] for i in res_per_veh[vehicle.id]]):
                        res.vehicle = vehicle
                        res_per_veh[vehicle.id].append(res.id)


        # loop for every vehicle through the list of reservations and look if a reservation can be added with a neighbour
        for vehicle in self.vehicles:
            for res in self.reservations:
                if LocalSearch.vehiclePossible(vehicle, res):
                    if not LocalSearch.doesListInterfere(res, [self.reservations[i] for i in res_per_veh[vehicle.id]]):
                        res.vehicle = vehicle
                        res_per_veh[vehicle.id].append(res.id)


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
    
    def checkNew(self, reservations: List[Reservation]) -> bool:
        for car in self.vehicles:
            if car.zone == None:
                # print(f"car {car.id} does not have a zone assigned")
                return False
            
        for res in reservations:
            # reservation is not filled in
            if res.vehicle == None:
                continue

            # two reservations for the same car intervene
            for indx, inter in enumerate(self.interferences[res.id]):
                if inter == True and res.vehicle == self.reservations[indx].vehicle:
                    # print(f"overlapping reservations r1: {res.id} | r2: {self.reservations[indx].id}")
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
    def carToZone(self, car: Vehicle, zone: Zone) -> List[Reservation]:
        changed_reservations: List[Reservation] = []

        if self.debug:
            print(f"switch to zone {zone}________________________")
        # delete reservations that will break
        for res in self.reservations:
            if res.vehicle == None:
                continue
            elif res.vehicle.id == car.id:
                if res.zone.id not in zone.neighbours and res.zone.id != zone.id:
                    if self.debug:
                        print(f"removed: res{res.id} res.zone {res.zone}")
                    res.vehicle = None
                    changed_reservations.append(res)

        for res in self.reservations:
            if res.vehicle is not None:
                if res.vehicle.id == car.id:
                   res.vehicle = None

        assigned = False
        for reservation in self.reservations:
            # assign all possible reservations for that zone
            if (reservation.zone.id == zone.id) and (reservation.vehicle is None):
                reservation.vehicle = car
                car.zone = zone
                assigned = True
                changed_reservations.append(reservation)

        for reservation in self.reservations:
            # also assign possible neigbours
            if reservation.vehicle is None and zone.id in reservation.zone.neighbours:
                reservation.vehicle = car
                car.zone = zone
                assigned = True
                changed_reservations.append(reservation)
                
        if not assigned and self.debug:
            print("not possible to assign vehicle to zone")

        return changed_reservations

    def switchCarToNeighbours(self, car: int) -> List[Reservation]:

        currentBestCost = self.calculateFullCosts()
        reservationsBest = deepcopy(self.reservations)
        vehiclesBest = deepcopy(self.vehicles)
        new_reservationsBest = reservationsBest
        new_vehiclesBest = vehiclesBest

        for z in self.vehicles[car].zone.neighbours:
            changedReservations: List[Reservation] = self.carToZone(self.vehicles[car], self.zones[z])
            cost = self.calculateFullCosts()

            # change is correct
            if cost < currentBestCost and self.checkNew(changedReservations):
                currentBestCost = cost
                new_reservationsBest = deepcopy(self.reservations)
                new_vehiclesBest = deepcopy(self.vehicles)
                print("found better cost")
            # change is not correct
            else:
                self.reservations = deepcopy(reservationsBest)
                self.vehicles = deepcopy(vehiclesBest)
                
        self.reservations = new_reservationsBest
        self.vehicles = new_vehiclesBest

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


    def printReservations(self):
        print("-----------------------------")
        for res in self.reservations:
            print(f"res{res.id} => {res.vehicle}")