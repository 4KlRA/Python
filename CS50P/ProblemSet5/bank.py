def main():
    print(value(input()))

def value(greeting):
    if(greeting[0: 5].upper() == "HELLO"): 
        return "$0"
    elif(greeting[0].upper() == 'H'): 
        return "$20"
    else:
        return "$100"


if __name__ == "__main__":
    main()