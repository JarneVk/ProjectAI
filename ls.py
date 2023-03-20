from typing import *
from DataStructure import *
from copy import deepcopy

import random


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
        self.res_to_veh: List[List[int]] = [[] for _ in range(len(vehicles))]
        self.debug = False

        self.stuckCount = 0
        self.prevCost = 1000000


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
                    self.res_to_veh[posVeh].append(res.id)

        self.sortReservationsID()

        # loop for every vehicle through the list of reservations sorted by zone and look if you can add more than 1
        for vehicle in self.vehicles:
            for res in self.reservations:
                if LocalSearch.vehiclePossible(vehicle, res):
                    if not LocalSearch.doesListInterfere(res, [self.reservations[i] for i in self.res_to_veh[vehicle.id]]):
                        res.vehicle = vehicle
                        self.res_to_veh[vehicle.id].append(res.id)


        # loop for every vehicle through the list of reservations and look if a reservation can be added with a neighbour
        for vehicle in self.vehicles:
            for res in self.reservations:
                if LocalSearch.vehiclePossible(vehicle, res):
                    if not LocalSearch.doesListInterfere(res, [self.reservations[i] for i in self.res_to_veh[vehicle.id]]):
                        res.vehicle = vehicle
                        self.res_to_veh[vehicle.id].append(res.id)
        
        print(self.res_to_veh)


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
    
    def calculateBestCosts(self) -> int:

        total_cost = 0
        for res in self.lastBestReservations:

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
    
    def calculatePartCost(reservations: List[Reservation]) -> int:

        cost_diff = 0
        for res in reservations:
            # res not assigned
            if res.vehicle == None:
                cost_diff += res.p1

            # res assigned car in own zone
            elif res.vehicle.zone == res.zone:
                cost_diff += 0

            # res assigned in car in neighbouring zone 
            elif res.vehicle.zone.id in res.zone.neighbours:
                cost_diff += res.p2
        
        return cost_diff
    
    def calculateCost(reservation: Reservation) -> int:
        # res not assigned
        if reservation.vehicle == None:
            return reservation.p1

        # res assigned car in own zone
        elif reservation.vehicle.zone == reservation.zone:
            return 0

        # res assigned in car in neighbouring zone 
        elif reservation.vehicle.zone.id in reservation.zone.neighbours:
            return reservation.p2
    
    
    # localSearch
    def carToZone(self, car: Vehicle, zone: Zone) -> List[Reservation]:
        changed_reservations: List[Reservation] = []

        if self.debug:
            print(f"switch {car.id} to zone {zone.id}________________________")
        
        # delete reservations that will break
        self.res_to_veh[car.id] = []

        for res in self.reservations:
            if res.vehicle is not None:
                if res.vehicle.id == car.id:
                   res.vehicle = None


        assigned = False
        for reservation in self.reservations:
            # assign all possible reservations for that zone
            if (reservation.zone.id == zone.id) and (reservation.vehicle is None) and (car.id in reservation.possibleVehicles):
                if not LocalSearch.doesListInterfere(reservation,changed_reservations):
                    reservation.vehicle = car
                    car.zone = zone
                    assigned = True
                    changed_reservations.append(reservation)
                    self.res_to_veh[car.id].append(reservation)
                

        #check for cars that can get a better cost
        for res in self.reservations:
            if reservation.vehicle != None:
                if(reservation.zone.id == zone.id) and (reservation.vehicle.zone.id != zone.id) and (car.id in reservation.possibleVehicles):
                    if not LocalSearch.doesListInterfere(res,changed_reservations):
                        reservation.vehicle = car
                        car.zone = zone
                        assigned = True
                        changed_reservations.append(reservation)
                        self.res_to_veh[car.id].append(reservation)


        for reservation in self.reservations:
            # also assign possible neigbours
            if reservation.vehicle is None and zone.id in reservation.zone.neighbours and (car.id in reservation.possibleVehicles):
                if not LocalSearch.doesListInterfere(reservation,changed_reservations):
                    reservation.vehicle = car
                    car.zone = zone
                    assigned = True
                    changed_reservations.append(reservation)
                    self.res_to_veh[car.id].append(reservation)
    

        if self.debug:
            self.printReservations()
        if not assigned and self.debug:
            print("not possible to assign vehicle to zone")

        return changed_reservations

    def switchCarToNeighbours(self, car: int) -> List[Reservation]:

        # self.lastBestReservations = deepcopy(self.reservations)
        # self.lastBestVehicles = deepcopy(self.vehicles)

        currentBestCost = self.calculateFullCosts()
        reservationsBest = deepcopy(self.reservations)
        vehiclesBest = deepcopy(self.vehicles)
        new_reservationsBest = reservationsBest
        new_vehiclesBest = vehiclesBest

        newCost = self.calculateFullCosts()
        if newCost - self.prevCost < 0:
            self.prevCost = newCost
            self.stuckCount =0
            opperator = "medium"
        elif self.stuckCount == 100:
            print("do big opp")
            opperator = "big"

        else:
            opperator = "medium"
            self.stuckCount +=1

        if opperator == "medium":
            for z in self.vehicles[car].zone.neighbours:
                changedReservations: List[Reservation] = self.carToZone(self.vehicles[car], self.zones[z])
                cost = self.calculateFullCosts()

                # change is correct
                if cost < currentBestCost and self.checkNew(changedReservations):
                    currentBestCost = cost
                    new_reservationsBest = deepcopy(self.reservations)
                    new_vehiclesBest = deepcopy(self.vehicles)
                    self.lastBestReservations = deepcopy(self.reservations)
                    self.lastBestVehicles = deepcopy(self.vehicles)
                    # print("found better cost")
                # change is not correct
                else:
                    self.reservations = deepcopy(self.lastBestReservations)
                    self.vehicles = deepcopy(self.lastBestVehicles)
            self.reservations = new_reservationsBest
            self.vehicles = new_vehiclesBest
        
        elif opperator == "big":
            changedReservations,_ = self.carZoneSwitch(self.vehicles[int(random.random()*len(self.vehicles))],self.vehicles[int(random.random()*len(self.vehicles))])
            self.prevCost = self.calculateFullCosts()
        
    
    def smallPPOperator(self, reservation: Reservation):
        # change vehicle from reservation
        None

    def carZoneSwitch(self, car1: Vehicle, car2: Vehicle) -> Tuple[List[Reservation], int]:

        if car1.zone is None or car2.zone is None:
            return [], 0

        zone1 = car1.zone
        zone2 = car2.zone

        changed_res: List[Reservation] = []
        changed_cost: int = 0

        self.res_to_veh[car1.id] = []
        self.res_to_veh[car2.id] = []

        # clear all reservations from both vehicles
        for res in self.reservations:
            if res.zone in [car1.zone, car2.zone]:
                changed_cost += LocalSearch.calculateCost(res)
                res.vehicle = None
                changed_res.append(res)

        # change zones
        car1.zone = zone2
        car2.zone = zone1

        res_car1: List[Reservation] = []
        # assign all possible reservations for car1
        for res in self.reservations:
            if res.zone == zone2:
                if LocalSearch.vehiclePossible(car1, res):
                    if not LocalSearch.doesListInterfere(res, res_car1):
                        res.vehicle = car1
                        res_car1.append(res)
                        changed_res.append(res)
                        self.res_to_veh[car1.id].append(res)
        
        res_car2: List[Reservation] = []
        # assign all possible reservations for car2
        for res in self.reservations:
            if res.zone == zone1:
                if LocalSearch.vehiclePossible(car2, res):
                    if not LocalSearch.doesListInterfere(res, res_car2):
                        res.vehicle = car2
                        res_car2.append(res)
                        changed_res.append(res)
                        self.res_to_veh[car2.id].append(res)

        # assign all possible neighbours to car1
        for res in self.reservations:
            if res.zone in car1.zone.neighbours:
                if LocalSearch.vehiclePossible(car1, res):
                    if not LocalSearch.doesListInterfere(res, res_car1):
                        res.vehicle = car1
                        res_car1.append(res)
                        changed_res.append(res)
                        self.res_to_veh[car1.id].append(res)

        # assign all possible neighbours to car2
        for res in self.reservations:
            if res.zone in car2.zone.neighbours:
                if LocalSearch.vehiclePossible(car2, res):
                    if not LocalSearch.doesListInterfere(res, res_car2):
                        res.vehicle = car2
                        res_car2.append(res)
                        changed_res.append(res)
                        self.res_to_veh[car2.id].append(res)

        return changed_res, changed_cost

    
    # output
    def writeOutput(self, filename: str):
        with open(filename, 'w') as file:
            file.write(f"{self.calculateBestCosts()}\n")
            file.write(f"+Vehicle assignments\n")

            for vehicle in self.lastBestVehicles:
                file.write(f"car{vehicle.id};z{vehicle.zone.id}\n")

            file.write("+Assigned requests\n")
            for reservation in self.lastBestReservations:
                if reservation.vehicle is None:
                    continue
                else:
                    file.write(f"req{reservation.id};car{reservation.vehicle.id}\n")

            file.write("+Unassigned requests\n")
            for reservation in self.lastBestReservations:
                if reservation.vehicle is None:
                    file.write(f"req{reservation.id}\n")


    def printReservations(self):
        print("-----------------------------")
        for res in self.reservations:
            print(f"res{res.id} zone {res.zone.id} posible {res.possibleVehicles}=> {res.vehicle}")