def main():
    time = input("What time is it? ")
    hour = convert(time)

    if(7 <= hour <= 8):
        print("breakfast time")
    elif(12 <= hour <= 13):
        print("lunch time")
    elif(18 <= hour <= 19):
        print("dinner time")

def convert(time):
    hour, min = time.split(":")
    hour = int(hour) + int(min)/60
    return hour


if __name__ == "__main__":
    main()