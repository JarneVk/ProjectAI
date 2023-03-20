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

    random.seed(args.seed)

    init_time = 0
    init_cost = 0

    reservations, zones, vehicles, interferences = parser_1.read_file(args.file)
    ls = LocalSearch(reservations, zones, vehicles, interferences, debug = args.verbose)
    ls.active = True
    
    start_time = time.perf_counter()
    itt = 0
    def run():
        ls.active = False
        end_time = time.perf_counter()

        print("last solution is :" + str(ls.checkNew(ls.lastBestReservations)))
        print(init_cost, " => ", ls.calculateBestCosts())

        ls.writeOutput(os.path.join("output", os.path.split(args.file)[-1]))

        print(f"itterations : {itt}")
        print("init time: {time:.4f}".format(time=(init_time-start_time)))
        print("end  time: {time:.4f}".format(time=(end_time-start_time)))

        

    timer = th.Timer(args.time, run)
    timer.start()

    init_time = time.perf_counter()

    ls.initialise()

    init_cost = ls.calculateFullCosts()

    print("initial solution: ",ls.checkAll())

    amount_v = len(ls.vehicles)
    prevcost = 0
    while(ls.active):
        # select a random vehicle
        ls.switchCarToNeighbours(int(random.random()*amount_v))
        itt += 1
    

if __name__ == "__main__":
    main()
