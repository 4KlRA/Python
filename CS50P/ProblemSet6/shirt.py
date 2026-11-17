import sys
from PIL import Image, ImageOps
import os

if(len(sys.argv) != 3):
    if(len(sys.argv) > 3):
        sys.exit("Too many command-line arguments")
    else:
        sys.exit("Too few command-line arguments")

in_path = sys.argv[1]
out_path = sys.argv[2]

valid_exts = [".jpg", ".jpeg", ".png"]
in_ext = os.path.splitext(in_path)[1].lower()
out_ext = os.path.splitext(out_path)[1].lower()

if in_ext not in valid_exts:
    sys.exit("Invalid input")
if out_ext not in valid_exts:
    sys.exit("Invalid output")
if in_ext != out_ext:
    sys.exit("Input and output have different extensions")

try:
   with Image.open(in_path) as person, Image.open("shirt.png") as shirt:
        fitted = ImageOps.fit(person, shirt.size)
        fitted.paste(shirt, shirt)
        fitted.save(out_path)

except FileNotFoundError:
    sys.exit("Input doesn't exist")