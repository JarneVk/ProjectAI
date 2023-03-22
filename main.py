import parser_1
import time
import sys
import os
from pprint import pprint
import argparse
import signal
import random
import threading as th

from ls import LocalSearch


def main():
    #############################################################################
    #
    #                           initialise
    #
    #############################################################################

    parser = argparse.ArgumentParser(prog='LocalSearch', description='LocalSearch algorithm')

    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-f', '--file', help='the filepath relative to the main.py file', default=os.path.join('input', 'toy1.csv'))
    parser.add_argument('-t', '--time', help='the amount of time (seconds) the algorithm may run', type=int, default=1)
    parser.add_argument('-s', '--seed',help='give a seed for the random number generator', type=int, default=69)

    args = parser.parse_args()

    if args.seed != 69:
        random.seed(args.seed)

    init_time = 0
    init_cost = 0

    reservations, zones, vehicles, interferences = parser_1.read_file(args.file)
    ls = LocalSearch(reservations, zones, vehicles, interferences, debug = args.verbose)
    ls.active = True
    
    start_time = time.perf_counter()
    lowest_cost = 0

    def run():

        end_time = time.perf_counter()

        print("last solution is: " + str(ls.checkNew(ls.lastBestReservations)))
        print(ls.checkAll())
        print(init_cost, " => ", ls.currentBestCostSmall)

        ls.writeOutput(os.path.join("output", os.path.split(args.file)[-1]))

        print("init time: {time:.4f}".format(time=(init_time-start_time)))
        print("end  time: {time:.4f}".format(time=(end_time-start_time)))

        print(lowest_cost)

        ls.active = False

    timer = th.Timer(args.time, run)
    timer.start()

    init_time = time.perf_counter()

    ls.initialise()

    init_cost = ls.calculateFullCosts()

    print("initial solution: ",ls.checkAll())

    last_costs = [init_cost, 0, 0, 0, 0]
    lowest_cost = init_cost

    cost = ls.calculateFullCosts()

    amount_v = len(ls.vehicles)
    while(ls.active):
        # select a random vehicle
        while(last_costs[0] != cost):
            ls.switchCarToNeighbours(int(random.random()*amount_v))
            cost = ls.calculateFullCosts()
            if cost < lowest_cost:
                lowest_cost = cost
            last_costs.pop(0)
            last_costs.append(cost)

        
        #     # print("plateau found at: ", ls.calculateFullCosts())
        ls.optimise()
        print("cost after optimisation: ", ls.calculateFullCosts())
        if ls.calculateFullCosts() < lowest_cost:
            lowest_cost = ls.calculateFullCosts()
        ls.initialise()
            # ls.initialise()
        #     # for _ in range(len(ls.reservations) * 10):
        #         # ls.smallPPOperator(ls.reservations[int(random.random()*len(ls.reservations))])
        #     cost = ls.calculateFullCosts()

        #     # if cost == last_cost:
        #         # ls.initialise()            
        last_costs.pop(0)
        last_costs.append(cost)        

if __name__ == "__main__":
    main()
