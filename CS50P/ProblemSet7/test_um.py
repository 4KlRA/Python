from um import count


def test_single_and_multiple_um():
  assert count("um") == 1
  assert count("um?") == 1
  assert count("um, hello, um, world") == 2
  assert count("um... um... um...") == 3


def test_case_insensitivity():
  assert count("Um, thanks for the album.") == 1
  assert count("Um, thanks, um...") == 2
  assert count("UM, hello UM!") == 2


def test_words_containing_um():
  # Must return 0 when "um" is part of another word
  assert count("yummy") == 0
  assert count("album") == 0
  assert count("umbrella") == 0
  assert count("instrumentation") == 0
