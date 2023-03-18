import parser_1
import time
import sys
import os
from pprint import pprint
import argparse
import threading
import signal

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

    args = parser.parse_args()

    signal.signal(signal.SIGBREAK, signal_catcher)

    x = threading.Thread(target=thread_function, args=(args.time, ))
    x.start()

    try:
        start_time = time.perf_counter()

        reservations, zones, vehicles, interferences = parser_1.read_file(args.file)

        ls = LocalSearch(reservations, zones, vehicles, interferences, debug = args.verbose)

        init_time = time.perf_counter()

        ls.initialise()

        init_cost = ls.calculateFullCosts()

        print("initial solution: ",ls.checkAll())

        while(True):
            for i in range(len(ls.vehicles)):
                ls.switchCarToNeighbours(i)

    except Exception as ex:
        print("Timeout catched!")

    finally:
        end_time = time.perf_counter()

        print("last solution is :" + str(ls.checkNew(ls.lastBestReservations)))
        print(init_cost, " => ", ls.calculateFullCosts())

        ls.writeOutput(os.path.join("output", os.path.split(args.file)[-1]))

        print(f"init time: {init_time-start_time}")
        print(f"end  time: {end_time-start_time}")

if __name__ == "__main__":
    main()
