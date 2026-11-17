import sys
from tabulate import tabulate
import csv

if(len(sys.argv) != 2):
    if(len(sys.argv) > 2):
        sys.exit("Too many command-line arguments")
    else:
        sys.exit("Too few command-line arguments")

path = sys.argv[1]
if(path[-4:] != ".csv"):
    sys.exit("Not a CSV file")

try:
    with open(path, "r") as file:
        reader = csv.reader(file)
        data = list(reader)
        print(tabulate(data, headers="firstrow", tablefmt="grid"))
except FileNotFoundError:
    sys.exit("File doesn't exist")