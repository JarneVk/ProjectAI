import DataStructure

def CalculateCosts(reservatorions:list[DataStructure.Reservation]):

    for res in reservatorions:
        if res.vehiecel.zone.id == res.zone.id:
            res.p1 = 10
            res.p2 = 5
        elif res.vehiecel.zone.id in res.zone.neighbours:
            res.p1 = 15
            res.p2 = 7
        else:
            res.p1 = 5
            res.p2 = 2
