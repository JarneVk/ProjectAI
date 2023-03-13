from typing import *
import DataStructure


def CheckAll(reservationList: List[DataStructure.Reservation], cars: List[DataStructure.Vehicle], resInterferList: List[List[bool]]) -> bool:

    for car in cars:
        # every car needs a zone
        if car.zone == None:
            print(f"auto {car.id} does not have a zone assigned")
            return False
        
    for res in reservationList:

        # reservation is not filled in
        if res.vehicle == None:
            continue

        # two reservations for the same car intervene
        for indx, inter in enumerate(resInterferList[res.id]):
            if inter == True and res.vehicle == reservationList[indx].vehicle:
                print(f"overlapping reservations r1: {res.id} | r2: {reservationList[indx].id}")
                return False

    return True

def CheckCarSwitch(car1:DataStructure.Vehicle,car2:DataStructure.Vehicle)->bool:
    if car1.zone == None or car2.zone == None:
        return False
    return True

def CheckResSwitch(res1:DataStructure.Reservation,res2:DataStructure.Reservation,reservationList:list[DataStructure.Reservation],resInterferList:list[bool])->bool:
    #reservations for a car can interfier with other reservations that where not in the swap
    #search in matrix for interferences on the car
    if res1.vehiecel == None or res2.vehiecel == None:
        return True
    for indx,inter in enumerate(resInterferList[res1.id]):
        if inter == True and res1.vehiecel == reservationList[indx].vehiecel:
            return False
    for indx,inter in enumerate(resInterferList[res2.id]):
        if inter == True and res2.vehiecel == reservationList[indx].vehiecel:
            return False
        
    if res1.zone not in res1.vehiecel.zone.neighbours:
            return False
    if res2.zone not in res2.vehiecel.zone.neighbours:
            return False

    return True
    

        

