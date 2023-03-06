import csv
import pprint
from DataStructure import *

with open("input/100_5_14_25.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=";")
    
    amount_requests: int = 0
    amount_zones: int = 0
    amount_vehicles: int = 0
    list_reservations = []
    list_zones = []
    list_vehicles = []
    
    for i, row in enumerate(csv_reader):
        if i == 0:
            amount_requests = int(row[0].split(": ")[1])
            # print(f"aantal requests: {amount_requests}")
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
        
        if i <= amount_requests + amount_zones + amount_vehicles + 1:
            # reading vehicles
            list_vehicles.append(Vehicle(int(row[0].strip("car"))))
        
    pprint.pprint(list_reservations)
    pprint.pprint(list_zones)
    pprint.pprint(list_vehicles)