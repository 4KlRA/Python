string = input("Input: ")
ans = ""

for char in string:
    if(char.lower() in ['a', 'e', 'i', 'o', 'u']):
        continue
    ans += char

print("Output: ", ans)