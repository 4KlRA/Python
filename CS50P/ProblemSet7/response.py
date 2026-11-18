from validator_collection import checkers

def main():
    validate(input("What's your email address? "))
    

def validate(email):
    if(checkers.is_email(email)):
        print("Valid")
    else:
        print("Invalid")


if __name__ == "__main__":
    main()