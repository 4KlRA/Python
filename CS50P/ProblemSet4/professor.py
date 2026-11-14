import random

def main():
    lvl = get_level()
    problems = generate_integer(lvl)
    score = 0;
    for id in problems:
        if(guess(problems[id][0], problems[id][1])):
            score += 1

    print(f"Score: {score}")

def get_level():
    while True:
        try:
            num = int(input("Level: "))
            if(num > 0 and num < 4):
                return num
        except (ValueError):
            pass


def generate_integer(level):
    pairs = {}
    for i in range(10):
        x = random.randint(1, 10 ** level)
        y = random.randint(1, 10 ** level)
        pairs[i + 1] =  [x, y]
    return pairs

def guess(x, y):
    tries = 0
    while tries < 3:
        try:
            ans = int(input(f"{x} + {y} = "))
            if(x + y == ans):
                return True
            else:
                print("EEE")
                tries += 1
        except ValueError:
            print("EEE")
            tries += 1
    print(f"{x} + {y} = {x + y}")
    return False

if __name__ == "__main__":
    main()