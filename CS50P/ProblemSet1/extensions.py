x = input("File: ")

y = x.split(sep='.')
y = y[-1].upper()

if(y == "GIF"): 
    print("image/gif")
elif(y == "JPEG" or y == "JPG"): 
    print("image/jpeg")
elif(y == "PNG"):
    print("image/png")
elif(y  == "PDF"):
    print("application/pdf")
elif(y == "TXT"):
    print("text/plain")
elif(y == "ZIP"):
    print("application/zip")
else:
    print("application/octet-stream")