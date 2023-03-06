import csv

with open("input/100_5_14_25.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=";")
    
    for i, row in enumerate(csv_reader):
        if i == 0:
            print(f"Column names are: {';'.join(row)}")
        else:
            print(f"row {i}: {';'.join(row)}")
