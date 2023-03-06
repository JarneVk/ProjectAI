import DataStructure


def CheckAll(reservationList:list[DataStructure.Reservation],cars:list[DataStructure.Vehicle],resInterferList:list[bool][bool]) -> bool:

    for car in cars:
        #every car needs a zone
        if car.zone == None:
            return False

    for res in reservationList:    
        #two cars can't overlop in time
        for indx,inter in enumerate(resInterferList[res.id]):
            if inter == True and res.vehiecel == reservationList[indx].vehiecel:
                return False

    return True

def CheckCarSwitch(car1:DataStructure.Vehicle,car2:DataStructure.Vehicle)->bool:
    if car1.zone == None or car2.zone == None:
        return False
    return True

def CheckResSwitch(res1:DataStructure.Reservation,res2:DataStructure.Reservation,reservationList:list[DataStructure.Reservation],resInterferList:list[bool][bool])->bool:
    #reservations for a car can interfier with other reservations that where not in the swap
    #search in matrix for interferences on the car
    for indx,inter in enumerate(resInterferList[res1.id]):
        if inter == True and res1.vehiecel == reservationList[indx].vehiecel:
            return False
    for indx,inter in enumerate(resInterferList[res2.id]):
        if inter == True and res2.vehiecel == reservationList[indx].vehiecel:
            return False
    return True
    

        

