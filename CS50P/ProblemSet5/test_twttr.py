from twttr import shorten

def test_basic():
    assert shorten("twitter") == "twttr"
    assert shorten("hello") == "hll"
    assert shorten("python") == "pythn"

def test_uppercase():
    assert shorten("TWITTER") == "TWTTR"
    assert shorten("HELLO") == "HLL"

def test_mixed_case():
    assert shorten("TwItTeR") == "TwtTR"

def test_numbers():
    assert shorten("12345") == "12345"
    assert shorten("h3ll0") == "h3ll0"

def test_punctuation():
    assert shorten("hello, world!") == "hll, wrld!"
    assert shorten("CS50!") == "CS50!"

def test_empty():
    assert shorten("") == ""
