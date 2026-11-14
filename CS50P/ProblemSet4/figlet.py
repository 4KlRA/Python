import sys
import pyfiglet

font = "big"

if(len(sys.argv) == 1):
    pass
elif(len(sys.argv) == 3 and sys.argv[1] in ["-f", "--font"]):
    font = sys.argv[2]
else:
    sys.exit("Invalid usage")

try: 
    figlet = pyfiglet.Figlet(font)
except pyfiglet.FontNotFound:
    sys.exit("Invalid Font")

text = input("Input: ")
output = figlet.renderText(text)

print("Output:\n" + output)