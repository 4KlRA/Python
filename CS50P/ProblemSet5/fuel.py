def main():
    exp = input("Fraction: ")
    print(check(exp))

def check(exp):
    while True:
        try: 
            x, y = exp.split("/")
            x = int(x)
            y = int(y)
            if (x < 0 or y <= 0 or x > y):
                exp = input("Fraction: ")
                continue
            percent = round(x / y * 100)
            if(percent <= 1): return "E"
            elif(percent >= 99): return "F"
            else: return (f"{percent}%")
        except (ValueError, ZeroDivisionError):
            pass

if __name__ == "__main__":
    main()