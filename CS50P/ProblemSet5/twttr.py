def main():
    print(shorten(input("Input: ")))


def shorten(word):
    ans = ""

    for char in word:
      if(char.lower() in ['a', 'e', 'i', 'o', 'u']):
          continue
      ans += char

    return ans


if __name__ == "__main__":
    main()