import re


def main():
  print(convert(input("Hours: ")))


def convert(s):
  pattern = r"^([1-9]|1[0-2])(?::([0-5]\d))? (AM|PM) to ([1-9]|1[0-2])(?::([0-5]\d))? (AM|PM)$"
  match = re.search(pattern, s)

  if not match:
    raise ValueError("Invalid time format")

  start_hr, start_min, start_period, end_hr, end_min, end_period = match.groups()

  start_24 = format_24(start_hr, start_min, start_period)
  end_24 = format_24(end_hr, end_min, end_period)

  return f"{start_24} to {end_24}"


def format_24(hour, minute, period):
  hr = int(hour)
  mins = minute if minute is not None else "00"

  if period == "AM":
    if hr == 12:
      hr = 0
  elif period == "PM":
    if hr != 12:
      hr += 12

  return f"{hr:02}:{mins}"


if __name__ == "__main__":
  main()