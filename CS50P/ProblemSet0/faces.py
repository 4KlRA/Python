def convert(string):
    string = string.replace(":)", "🙂")
    string = string.replace(":(", "🙁")
    return string

def main():
    string = str(input("Enter a text: "))
    print(convert(string))

main()