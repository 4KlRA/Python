import random

def getNumber(text):
    while True:
        try:
            num = int(input(text))
            if(num > 0):
                return num
        except (ValueError):
            pass


lvl = getNumber("Level: ")

num = random.randint(1, lvl)


while True:
    guess = getNumber("Guess: ")
    if(guess < num):
        print("too small!")
    elif(guess > num):
        print("TOO LARGE!")
    else:
        print("Just Right!")
        break