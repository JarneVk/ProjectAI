import DataStructure


def CheckAll(reservationList:list[DataStructure.Reservation],cars:list[DataStructure.Vehicle],resInterferList:list[bool]) -> bool:

    for car in cars:
        #every car needs a zone
        if car.zone == None:
            print("geen zone toegekent aan auto")
            return False
        
    for res in reservationList:    
        if res.vehiecel == None:
            break
        #two cars can't overlop in time
        for indx,inter in enumerate(resInterferList[res.id]):
            if inter == True and res.vehiecel == reservationList[indx].vehiecel:
                print(f"overlappende reservaties r1: {res} | r2: {reservationList[indx]} | index {indx},{res.id}")
                return False
        
        #check if car is in nabourzone
        if res.zone not in res.vehiecel.zone.neighbours and res.zone != res.vehiecel.zone.id:
            print(f"car {res} not in nabour zone {res.vehiecel.zone}")
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
    

        

