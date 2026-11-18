import re


def main():
    print(parse(input("HTML: ")))


def parse(s):
    pattern = r'<iframe[^>]*\bsrc="https?://(?:www\.)?youtube\.com/embed/([a-zA-Z0-9_-]+)"'
    if match := re.search(pattern, s):
        return f"https://youtub.be/{match.group(1)}"
    return None


if __name__ == "__main__":
    main()