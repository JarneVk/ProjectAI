import DataStructure


def CheckAll(reservationList:list[DataStructure.Reservation],cars:list[DataStructure.Vehiecels]) -> bool:

    for car in cars:
        if car.zone == None:
            return False

