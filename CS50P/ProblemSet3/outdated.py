months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]

while True:
    try:
        date = input("Date: ").strip()
        if "/" in date:
            month, day, year = date.split("/")
        elif "," in date:
            month, day, year = date.replace(",", "").split(" ")
            month = months.index(month) + 1
        else:
            continue

        if(1 <= int(month) <= 12 and 1 <= int(day) <= 31):
            print(f"{year}-{int(month):02}-{int(day):02}")
    except ValueError:
        pass
    except KeyboardInterrupt:
        break