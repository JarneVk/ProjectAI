import parser_1
import DataStructure
import cost
import control
import init
import output


def main():
    #############################################################################
    #
    #                           initialise
    #
    #############################################################################
    reservations, zones, vehicles, interferences = parser_1.read_file('input/100_5_14_25.csv')

    reservations, vehicles = init.initialise(reservations, zones, vehicles)
    output.writeOutput(reservations, zones, vehicles, cost.CalculateCosts(reservations, zones))

    #make start solution
    print(control.CheckAll(reservations, vehicles, interferences))
    print(cost.CalculateCosts(reservations, zones))

if __name__ == "__main__":
    main()
