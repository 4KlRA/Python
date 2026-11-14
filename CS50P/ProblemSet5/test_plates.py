
from plates import is_valid

def test_length():
    assert is_valid("AB") == True
    assert is_valid("ABCDEF") == True
    assert is_valid("A") == False
    assert is_valid("ABCDEFG") == False

def test_start():
    assert is_valid("12AB") == False
    assert is_valid("A123") == False

def test_numbers():
    assert is_valid("CS50") == True
    assert is_valid("CS05") == False
    assert is_valid("CS50P") == False
    assert is_valid("AAA222") == True

def test_punctuation():
    assert is_valid("AB!2") == False
    assert is_valid("AB 12") == False
    assert is_valid("AB.12") == False

def test_letters():
    assert is_valid("HELLO") == True
    assert is_valid("ABC123") == True
