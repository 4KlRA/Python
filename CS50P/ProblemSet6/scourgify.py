import sys
import csv

if(len(sys.argv) != 3):
    if(len(sys.argv) > 3):
        sys.exit("Too many command-line arguments")
    else:
        sys.exit("Too few command-line arguments")

in_path = sys.argv[1]
out_path = sys.argv[2]

if(in_path[-4:] != ".csv" and out_path[-4:] != ".csv"):
    sys.exit("Not a CSV file")

try:
    with open(in_path, "r") as inp:
        reader = csv.DictReader(inp)
        with open(out_path, "w", newline="") as out:
            writer = csv.DictWriter(out, fieldnames=["first", "last", "house"])
            writer.writeheader()
            for row in reader:
                last, first = row["name"].split(", ")
                writer.writerow({"first": first, "last": last, "house": row["house"]})

except FileNotFoundError:
    sys.exit(f"Couldn't read {in_path}")