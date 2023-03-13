import parser_1
import DataStructure
import cost
import control


def main():
    #############################################################################
    #
    #                           initialise
    #
    #############################################################################
    lists = parser_1.read_file('input/100_5_14_25.csv')

    #make start solution
    print(control.CheckAll(lists[0],lists[2],lists[3]))
    print(cost.CalculateCosts(lists[0],lists[1]))

if __name__ == "__main__":
    main()
