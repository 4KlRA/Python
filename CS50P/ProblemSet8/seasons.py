from datetime import date
import sys
import inflect

p = inflect.engine()


def main():
  dob = input("Date of Birth: ").strip()
  try:
    print(convert(dob))
  except (ValueError, OverflowError, OSError):
    sys.exit("Invalid date")


def convert(dob):
  if len(dob) != 10:
    raise ValueError("Invalid date")
  dob = date.fromisoformat(dob)
  today = date.today()
  if dob > today:
    raise ValueError("Date cannot be in the future")
  minutes = (today - dob).days * 24 * 60
  words = p.number_to_words(minutes, andword="")
  return f"{words.capitalize()} minutes"


if __name__ == "__main__":
  main()
