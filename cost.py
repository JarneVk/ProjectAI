import DataStructure

def CalculateCosts(reservatorions:list[DataStructure.Reservation],zones:list[DataStructure.Zone]):

    p1_tot = 0
    p2_tot = 0
    for res in reservatorions:
        #res not assigned
        if res.vehiecel == None:
            res.p1 = 10
            res.p2 = 5
            p1_tot += 10
            p2_tot += 5
        elif res.vehiecel.zone.id == res.zone:
            res.p1 = 15
            res.p2 = 7
            p1_tot += 15
            p2_tot += 7
        elif res.vehiecel.zone.id in zones(res.zone):
            res.p1 = 5
            res.p2 = 2
            p1_tot += 5
            p2_tot += 2

    return p1_tot,p2_tot
