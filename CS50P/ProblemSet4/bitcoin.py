import requests
import sys


if len(sys.argv) != 2:
    sys.exit("Missing command-line argument")
try:
    quantity = float(sys.argv[1])
except (ValueError):
    sys.exit("Command-line argument is not a number")

try:
    #Api key is already deleted so don't try anything funny
    response = requests.get("https://rest.coincap.io/v3/assets/bitcoin?apiKey=d178d1534800c77a53348d1e3df542405c62d299e4f7f5659eb32ef910b51e00")
    data = response.json()
    price = float(data["data"]["priceUsd"])
except requests.RequestException:
    sys.exit("Error querying API")

total = quantity * price
print(f"{total:,.4f}")