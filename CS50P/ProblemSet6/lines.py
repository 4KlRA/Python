import sys

if(len(sys.argv) != 2):
    if(len(sys.argv) > 2):
        sys.exit("Too many command-line arguments")
    else:
        sys.exit("Too few command-line arguments")

path = sys.argv[1]
if(path[-3:] != ".py"):
    sys.exit("Not a python file")

count = 0

try:
    with open(path, "r") as file:
        for line in file:
            count += 1
except FileNotFoundError:
    sys.exit("File doesn't exist")

print(count)