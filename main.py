import parser_1
import DataStructure
import cost
import control
import init
import output
import time
import sys
import os
import pprint
import localSearch

from ls import LocalSearch


def main():
    #############################################################################
    #
    #                           initialise
    #
    #############################################################################
    start_time = time.perf_counter()

    if len(sys.argv) > 1:
        filename = os.path.split(sys.argv[-1])
    else:
        filename = ["input", "toy1.csv"]

    reservations, zones, vehicles, interferences = parser_1.read_file(os.path.join("input", filename[-1]))

    ls = LocalSearch(reservations, zones, vehicles, interferences)

    ls.initialise()
    print("initial solution: ",ls.checkAll())
    for i in range(len(ls.vehicles)):
        ls.switchCarToNeighbours(ls.vehicles[i])

    print(ls.calculateFullCosts())

    # reservations, vehicles = init.initialise(reservations, zones, vehicles, interferences)

    # output.writeOutput(os.path.join("output", "temp1.csv"), reservations, zones, vehicles, cost.CalculateCosts(reservations, zones))

    # # reservations = localSearch.switchCarToNeighbours(car = vehicles[0], reservations = reservations, zones = zones, costFunction = cost.CalculateCosts)

    # output.writeOutput(os.path.join("output", filename[-1]), reservations, zones, vehicles, cost.CalculateCosts(reservations, zones))

    # #make start solution
    # init_time = time.perf_counter()
    # print(control.CheckAll(reservations, vehicles, interferences))
    # print(cost.CalculateCosts(reservations, zones))

    # end_time = time.perf_counter()

    # print(f"init time: {init_time-start_time}")
    # print(f"end  time: {end_time-start_time}")

if __name__ == "__main__":
    main()
