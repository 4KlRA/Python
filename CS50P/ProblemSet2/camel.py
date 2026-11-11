camel_case = input("camelCase: ")
snake_case = ""

for i in camel_case:
    if(i.isupper()):
        snake_case += "_"
    snake_case += i.lower()

print("snake_case: ", snake_case)