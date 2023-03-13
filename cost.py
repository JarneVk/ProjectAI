import DataStructure

def CalculateCosts(reservatorions:list[DataStructure.Reservation],zones:list[DataStructure.Zone]):

    for res in reservatorions:
        if res.vehiecel.zone.id == res.zone:
            res.p1 = 10
            res.p2 = 5
        elif res.vehiecel.zone.id in zones(res.zone):
            res.p1 = 15
            res.p2 = 7
        else:
            res.p1 = 5
            res.p2 = 2
