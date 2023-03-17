import parser_1
import DataStructure
import cost
import control
import init
import output
import time
import sys
import os
from pprint import pprint
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

    ls = LocalSearch(reservations, zones, vehicles, interferences, debug = False)

    init_time = time.perf_counter()

    ls.initialise()

    init_cost = ls.calculateFullCosts()

    print("initial solution: ",ls.checkAll())

    for _ in range(1):
        for i in range(len(ls.vehicles)):
            ls.switchCarToNeighbours(i)

    print(ls.checkAll())
    print(init_cost, " => ", ls.calculateFullCosts())

    ls.writeOutput(os.path.join("output", filename[-1]))

    end_time = time.perf_counter()

    print(f"init time: {init_time-start_time}")
    print(f"end  time: {end_time-start_time}")

if __name__ == "__main__":
    main()
