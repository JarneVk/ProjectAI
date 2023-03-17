import csv
import pprint
from DataStructure import *
import DataStructure
import numpy as np
from typing import *

def read_file(filepath: str, debug: bool = False) -> Tuple[List[DataStructure.Reservation], List[DataStructure.Zone], List[DataStructure.Vehicle], List[bool]]:
    with open(filepath) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=";")
        
        amount_requests: int = 0
        amount_zones: int = 0
        amount_vehicles: int = 0
        list_reservations: List[Reservation] = []
        list_zones: List[Zone] = []
        list_vehicles: List[Vehicle] = []
        
        for i, row in enumerate(csv_reader):
            if i == 0:
                amount_requests = int(row[0].split(": ")[1])
                continue
            
            if i <= amount_requests:
                # reading reservations
                ID = int(row[0][3:])
                zone = int(row[1].strip("z"))
                day = int(row[2])
                start = int(row[3])
                restime = int(row[4])
                possibleVehicels = [int(x.strip("car")) for x in row[5].split(",")]
                p1 = int(row[6])
                p2 = int(row[7])
                list_reservations.append(Reservation(ID, zone, day, start, restime,
                                                    possibleVehicels, p1, p2))
                continue
            if i == amount_requests + 1:
                amount_zones = int(row[0].split(": ")[1])
                continue
            
            if i <= amount_requests + amount_zones + 1:
                # reading zones
                list_zones.append(Zone(int(row[0].strip("z")), [int(x.strip('z')) for x in row[1].split(",")]))
                continue
            
            if i == amount_requests + amount_zones + 2:
                amount_vehicles = int(row[0].split(": ")[1])
                continue
            
            if i <= amount_requests + amount_zones + amount_vehicles + 2:
                # reading vehicles
                list_vehicles.append(Vehicle(int(row[0].strip("car"))))
            
        if debug:
            pprint.pprint(list_reservations)
            pprint.pprint(list_zones)
            pprint.pprint(list_vehicles)

        for res in list_reservations:
            zone_id = res.zone
            res.zone = list_zones[zone_id]

        #make reservation interference list
        interList = reservationInterfeer(list_reservations)

        return list_reservations, list_zones, list_vehicles, interList
    
def doesInterfere(res1: DataStructure.Reservation, res2: DataStructure.Reservation) -> bool:
    # interference if start AND/OR end of second is in duration of first reservation

    start_1 = res1.start
    end_1 = res1.start + res1.restime
    start_2 = res2.start
    end_2 = res2.start + res2.restime

    if start_1 < start_2 and start_2 < end_1:
        return True
    elif start_1 < end_2 and end_2 < end_1:
        return True
    return False

def reservationInterfeer(resList:list[DataStructure.Reservation]):
    interList = [[False for x in range(len(resList))] for y in range(len(resList))]

    for idx1,res1 in enumerate(resList):
        for idx2,res2 in enumerate(resList):
            if res1.id == res2.id:
                continue
            
            elif res1.day == res2.day:
                interList[idx1][idx2] = doesInterfere(res1, res2)
    return interList