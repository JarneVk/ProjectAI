from typing import *
from DataStructure import *
from copy import deepcopy
from pprint import pprint
import random
from datetime import datetime

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
    
    def vehiclePossibleOwn(vehicle: Vehicle, res: Reservation) -> bool:
        return res.zone.id == vehicle.zone.id and res.vehicle is None and vehicle.id in res.possibleVehicles
    
    def vehiclePossibleNeighbour(vehicle: Vehicle, res: Reservation) -> bool:
        return vehicle.zone.id in res.zone.neighbours and res.vehicle is None and vehicle.id in res.possibleVehicles


    def __init__(self, reservations: List[Reservation], zones: List[Zone], vehicles: List[Vehicle], interferences: List[List[bool]], debug: bool = False) -> None:
        self.reservations: List[Reservation] = reservations
        self.zones: List[Zone] = zones
        self.vehicles: List[Vehicle] = vehicles
        self.interferences: List[List[bool]] = interferences
        self.res_to_veh: List[List[Reservation]] = [[] for _ in range(len(vehicles))]
        self.debug = False

    def setVehicleIfNotInterfere(self, reservation: Reservation, vehicle: Vehicle):
            if not LocalSearch.doesListInterfere(reservation, self.res_to_veh[vehicle.id]):
                reservation.vehicle = vehicle
                self.res_to_veh[vehicle.id].append(reservation)

    # Initialisatie
    def initialise(self, random_bool = False):
        self.sortReservationsVehicles()

        self.res_to_veh = [[] for _ in range(len(self.vehicles))]
        for veh in self.vehicles:
            veh.zone = None
        for res in self.reservations:
            res.vehicle = None

        
        if random_bool:
            random.shuffle(self.reservations)
        used = []

        for res in self.reservations:
            for posVeh in res.possibleVehicles:
                if posVeh not in used:
                    used.append(posVeh)
                    res.vehicle = self.vehicles[posVeh]
                    self.vehicles[posVeh].zone = res.zone
                    self.res_to_veh[posVeh].append(res)

        self.sortReservationsID()

        # loop for every vehicle through the list of reservations sorted by zone and look if you can add more than 1

        for vehicle in self.vehicles:
            for res in self.reservations:
                if LocalSearch.vehiclePossibleOwn(vehicle, res):
                    self.setVehicleIfNotInterfere(res, vehicle)


        # loop for every vehicle through the list of reservations and look if a reservation can be added with a neighbour
        for vehicle in self.vehicles:
            for res in self.reservations:
                if LocalSearch.vehiclePossibleNeighbour(vehicle, res):
                # if vehicle.zone.id in res.zone.neighbours and res.vehicle is None and vehicle.id in res.possibleVehicles:
                    self.setVehicleIfNotInterfere(res, vehicle)

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
    
        else:
            return reservation.p1
        
    # localSearch

    def commit(self):
        self.currentBestRes = deepcopy(self.reservations)
        self.currentBestVeh = deepcopy(self.vehicles)

    def restore(self):
        self.reservations = deepcopy(self.currentBestRes)
        self.vehicles = deepcopy(self.currentBestVeh)

    def run(self):
        self.lastCosts = [0, 0, 0, 0, 0]
        threshold = 0
        age = 1

        self.currentBestRes = deepcopy(self.reservations)
        self.currentBestVeh = deepcopy(self.vehicles)

        self.bestBigCost = self.calculateFullCosts()
        self.smallestCost = deepcopy(self.bestBigCost)
        self.smallestRes = deepcopy(self.currentBestRes)
        self.smallestVeh = deepcopy(self.currentBestVeh)

        while self.active:

            vehicleId = int(random.random()*len(self.vehicles))
            localBestCost = self.bestBigCost
            localBestRes  = deepcopy(self.currentBestRes)
            localBestVeh  = deepcopy(self.currentBestVeh)

            for i in range(len(self.zones)):                
                # change vehicle to all zones and get best one
                changed_res, cost_change = self.carToZone(self.vehicles[vehicleId], self.zones[i])
                cost = self.calculateFullCosts()

                if self.checkNew(changed_res) and cost < localBestCost + threshold:
                    localBestCost = cost
                    localBestRes  = deepcopy(self.reservations)
                    localBestVeh  = deepcopy(self.vehicles)
                else:
                    self.reservations = deepcopy(localBestRes)
                    self.vehicles     = deepcopy(localBestVeh)

            cost = self.calculateFullCosts()
            if self.checkAll() and cost != self.bestBigCost and cost < self.bestBigCost + threshold:
                # new cost is lower than the threshold
                print(f"\nnew best cost found! {cost}")
                self.commit()

                age = 1

                self.bestBigCost = cost

                if self.bestBigCost < self.smallestCost:
                    self.smallestCost = self.bestBigCost
                    self.smallestRes = deepcopy(self.currentBestRes)
                    self.smallestVeh = deepcopy(self.currentBestVeh)
            
            else:
                print(f"age: {age}", end="\r")
                age *= 1.5

                self.restore()

                if age > 17:
                    print("reassign reservations")
                    self.BigOp_reassignReservations()
                    age = 1

                if age > 11:
                    self.carZoneSwitch(self.vehicles[int(random.random()*len(self.vehicles))], self.vehicles[int(random.random()*len(self.vehicles))])

                if age > 10:
                    if self.optimise():
                        cost = self.calculateFullCosts()
                        print(f"\nnew best small cost: {cost}")

                        if cost < self.smallestCost + threshold and self.checkAll():
                            self.smallestCost = cost
                            self.smallestRes = deepcopy(self.reservations)
                            self.smallestVeh = deepcopy(self.vehicles)
                        age /= 2

            threshold = (age * 2)
        
    def carToZone(self, car: Vehicle, zone: Zone) -> Tuple[List[Reservation], int]:
        changed_reservations: List[Reservation] = []
        cost_change = 0

        if self.debug:
            print(f"switch {car.id} to zone {zone.id}________________________")
        
        # delete reservations that will break
        self.res_to_veh[car.id] = []

        car.zone = zone

        for res in self.reservations:
            if res.vehicle is not None:
                if res.vehicle.id == car.id:
                #    cost_change -= LocalSearch.calculateCost(res)
                    res.vehicle = None

                    #check if deleted res can be assigned to car in his onw zone
                    for v in self.vehicles:
                        if v.zone == None:
                            continue
                        if (res.zone.id == v.zone.id) and (v.id in res.possibleVehicles):
                            vehres = []
                            for r in self.reservations:
                                if r.vehicle == None:
                                    continue
                                if r.vehicle.id == v.id:
                                    vehres.append(r)
                            if not LocalSearch.doesListInterfere(res, vehres):
                                res.vehicle = v
                                changed_reservations.append(res)
                                self.res_to_veh[v.id].append(res)
                                cost_change += LocalSearch.calculateCost(res)

        
        assigned = False
    
        for reservation in self.reservations:
            # assign all possible reservations for that zone
            if (reservation.zone.id == zone.id) and (reservation.vehicle is None) and (car.id in reservation.possibleVehicles):
                if not LocalSearch.doesListInterfere(reservation, self.res_to_veh[car.id]):
                    reservation.vehicle = car
                    assigned = True
                    changed_reservations.append(reservation)
                    self.res_to_veh[car.id].append(reservation)
                    cost_change += LocalSearch.calculateCost(reservation)

        #check for cars that can get a better cost
        for res in self.reservations:
            if reservation.vehicle != None:
                if(reservation.zone.id == zone.id) and (reservation.vehicle.zone.id != zone.id) and (car.id in reservation.possibleVehicles):
                    if not LocalSearch.doesListInterfere(res, self.res_to_veh[car.id]):
                        reservation.vehicle = car
                        assigned = True
                        changed_reservations.append(reservation)
                        self.res_to_veh[car.id].append(reservation)
                        cost_change += LocalSearch.calculateCost(reservation)


        for reservation in self.reservations:
            # also assign possible neigbours
            if reservation.vehicle is None and zone.id in reservation.zone.neighbours and (car.id in reservation.possibleVehicles):
                if not LocalSearch.doesListInterfere(reservation, self.res_to_veh[car.id]):
                    reservation.vehicle = car
                    assigned = True
                    changed_reservations.append(reservation)
                    self.res_to_veh[car.id].append(reservation)
                    cost_change += LocalSearch.calculateCost(reservation)
    

        if self.debug:
            self.printReservations()
        if not assigned and self.debug:
            print("not possible to assign vehicle to zone")

        return changed_reservations, cost_change

    def optimise(self) -> bool:
        optimised = False
        for i in range(len(self.reservations)):
            self.smallPPOperator(self.reservations[i])
            cost = self.calculateFullCosts()

            if cost < self.bestBigCost and self.checkAll():
                # better solution
                self.commit()
                self.bestBigCost = cost
                # print("optimised something")
                optimised = True
            else:
                self.restore()
        
        return optimised

    def smallPPOperator(self, reservation: Reservation):
        if LocalSearch.calculateCost(reservation) == 0:
            return
        # change vehicle from reservation to possible vehicle in own zone
        for vehicle in self.vehicles:
            if vehicle.zone == reservation.zone and vehicle.id in reservation.possibleVehicles and not LocalSearch.doesListInterfere(reservation, self.res_to_veh[vehicle.id]):
                reservation.vehicle = vehicle
                self.res_to_veh[vehicle.id].append(reservation)
                # print(f"switched res{reservation.id} to vehicle{vehicle.id}")
        
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
                if LocalSearch.vehiclePossibleOwn(car1, res):
                    if not LocalSearch.doesListInterfere(res, res_car1):
                        res.vehicle = car1
                        res_car1.append(res)
                        changed_res.append(res)
                        self.res_to_veh[car1.id].append(res)
        
        res_car2: List[Reservation] = []
        # assign all possible reservations for car2
        for res in self.reservations:
            if res.zone == zone1:
                if LocalSearch.vehiclePossibleOwn(car2, res):
                    if not LocalSearch.doesListInterfere(res, res_car2):
                        res.vehicle = car2
                        res_car2.append(res)
                        changed_res.append(res)
                        self.res_to_veh[car2.id].append(res)

        # assign all possible neighbours to car1
        for res in self.reservations:
            if res.zone in car1.zone.neighbours:
                if LocalSearch.vehiclePossibleNeighbour(car1, res):
                    if not LocalSearch.doesListInterfere(res, res_car1):
                        res.vehicle = car1
                        res_car1.append(res)
                        changed_res.append(res)
                        self.res_to_veh[car1.id].append(res)

        # assign all possible neighbours to car2
        for res in self.reservations:
            if res.zone in car2.zone.neighbours:
                if LocalSearch.vehiclePossibleNeighbour(car2, res):
                    if not LocalSearch.doesListInterfere(res, res_car2):
                        res.vehicle = car2
                        res_car2.append(res)
                        changed_res.append(res)
                        self.res_to_veh[car2.id].append(res)

        return changed_res, changed_cost
    
    
    def BigOp_reassignReservations(self):
        #remove all reservations 
        for r in self.reservations:
            r.vehicle = None

        random.shuffle(self.reservations)

        #reassign vehicles
        for res in self.reservations:
            for v in self.vehicles:
                if (res.zone.id == v.zone.id) and (v.id in res.possibleVehicles):
                            vehres = []
                            for r in self.reservations:
                                if r.vehicle == None:
                                    continue
                                if r.vehicle.id == v.id:
                                    vehres.append(r)
                            if not LocalSearch.doesListInterfere(res, vehres):
                                res.vehicle = v
                                self.res_to_veh[v.id].append(res)
                                continue


    
    # output
    def writeOutput(self, filename: str):
        with open(filename, 'w') as file:
            file.write(f"{self.smallestCost}\n")
            file.write(f"+Vehicle assignments\n")

            for vehicle in self.smallestVeh:
                file.write(f"car{vehicle.id};z{vehicle.zone.id}\n")

            file.write("+Assigned requests\n")
            for reservation in self.smallestRes:
                if reservation.vehicle is None:
                    continue
                else:
                    file.write(f"req{reservation.id};car{reservation.vehicle.id}\n")

            file.write("+Unassigned requests\n")
            for reservation in self.smallestRes:
                if reservation.vehicle is None:
                    file.write(f"req{reservation.id}\n")


    def printReservations(self):
        print("-----------------------------")
        for res in self.reservations:
            print(f"res{res.id} zone {res.zone.id} posible {res.possibleVehicles}=> {res.vehicle}")