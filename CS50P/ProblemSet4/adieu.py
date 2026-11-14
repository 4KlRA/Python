lst = []

try:
    while True:
        line = input("Name: ")
        lst.append(line)

except KeyboardInterrupt:
    print("\n")
    pass

output = "Adieu, adieu, to "

if(len(lst) >= 2):
    for i in range(0, len(lst) - 1):
        output += lst[i] + ", "

    output += f"and {lst[-1]}"
else:
    output += lst[0]

print(output)