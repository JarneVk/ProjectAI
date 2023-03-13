import parser_1
import DataStructure
import cost
import control
import init
import output
import time


def main():
    #############################################################################
    #
    #                           initialise
    #
    #############################################################################
    start_time = time.perf_counter()
    reservations, zones, vehicles, interferences = parser_1.read_file('input/toy1.csv')

    reservations, vehicles = init.initialise(reservations, zones, vehicles)
    output.writeOutput("output/toy1.csv", reservations, zones, vehicles, cost.CalculateCosts(reservations, zones))

    #make start solution
    init_time = time.perf_counter()
    print(control.CheckAll(reservations, vehicles, interferences))
    print(cost.CalculateCosts(reservations, zones))

    end_time = time.perf_counter()

    print(f"init time: {init_time-start_time}")
    print(f"end  time: {end_time-start_time}")

if __name__ == "__main__":
    main()
