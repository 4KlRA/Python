def main():
    plate = input("Plate: ")
    if is_valid(plate):
        print("Valid")
    else:
        print("Invalid")


def is_valid(s):
    return (
        is_valid_plate_length(s) and
        starts_with_two_letters(s) and
        check_number_position(s) and
        has_only_letters_and_numbers(s)
    )

def is_valid_plate_length(plate):
    return 2 <= len(plate) <= 6

def starts_with_two_letters(plate):
    return plate[0].isalpha() and plate[1].isalpha()

def check_number_position(plate):
    for i in range(len(plate)):
        if(plate[i].isdigit()):
            if(plate[i] == "0"): return False
            return plate[i:].isdigit()
    return True

def has_only_letters_and_numbers(plate):
    return plate.isalnum()

if __name__ == "__main__":
    main()