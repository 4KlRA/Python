parcha =  {}

while True:
    try:
        item = input()
        parcha[item.upper()] += 1 
    except (EOFError, KeyboardInterrupt):
        break
        break
    except KeyError:
        parcha.update({item.upper(): 1})


for item, count in sorted(parcha.items()):
    print(f"{count} {item}")