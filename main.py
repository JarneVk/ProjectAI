import parser_1
import time
import sys
import os
from pprint import pprint
import argparse
import threading
import signal
import random

from ls import LocalSearch

def thread_function(time_out):
    time.sleep(time_out)
    print("sending signal SIGINT now")
    signal.raise_signal(signal.SIGBREAK)

def signal_catcher(signum, stack_frame):
    print("catched signal")
    raise Exception("TIMEOUT")

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
    parser.add_argument('-s', '--seed',help='give a seed for the random number generator',type=int,default=69)

    args = parser.parse_args()

    signal.signal(signal.SIGBREAK, signal_catcher)

    x = threading.Thread(target=thread_function, args=(args.time, ))
    x.start()

    random.seed(10)

    try:
        start_time = time.perf_counter()

        reservations, zones, vehicles, interferences = parser_1.read_file(args.file)

        ls = LocalSearch(reservations, zones, vehicles, interferences, debug = False)

        init_time = time.perf_counter()

        ls.initialise()

        init_cost = ls.calculateFullCosts()

        print("initial solution: ",ls.checkAll())

        amount_v = len(ls.vehicles)
        while(True):
            #select a random vehicle
            ls.switchCarToNeighbours(int(random.random()*amount_v))

    except Exception as ex:
        print(f"exception {ex}")

    finally:
        end_time = time.perf_counter()

        print("last solution is :" + str(ls.checkNew(ls.lastBestReservations)))
        print(init_cost, " => ", ls.calculateFullCosts())

        ls.writeOutput(os.path.join("output", os.path.split(args.file)[-1]))

        print("init time: {time:.4f}".format(time=(init_time-start_time)))
        print("end  time: {time:.4f}".format(time=(end_time-start_time)))

if __name__ == "__main__":
    main()
