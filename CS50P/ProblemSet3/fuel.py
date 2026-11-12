while True:
    exp = input("Fraction: ")
    x, y = exp.split("/")
    try:
        percent = int(int(x) * 100/ int(y))
        if(int(x) < 0 or int(y) < 0 or int(x) > int(y)): continue
        break
    except ValueError:
        pass
    except ZeroDivisionError:
        pass

if(percent <= 1): print("E")
elif(percent == 100): print("F")
else: print(str(percent) + "%")