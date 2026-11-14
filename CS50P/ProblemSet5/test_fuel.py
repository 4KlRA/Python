from fuel import check

def test_empty():
    assert check("1/100") == "E"
    assert check("0/100") == "E"

def test_full():
    assert check("99/100") == "F"
    assert check("100/100") == "F"

def test_percentage():
    assert check("1/2") == "50%"
    assert check("3/4") == "75%"
    assert check("1/4") == "25%"

def test_rounding():
    assert check("2/3") == "67%"
    assert check("1/3") == "33%"
