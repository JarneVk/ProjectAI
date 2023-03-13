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
                ID = row[0]
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
    

def reservationInterfeer(resList:list[DataStructure.Reservation]):
    interList = [[False for x in range(len(resList))] for y in range(len(resList))]

    for res in resList:
        pass