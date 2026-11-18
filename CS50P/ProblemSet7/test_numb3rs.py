from numb3rs import validate


def test_valid_ips():
  assert validate("127.0.0.1") == True
  assert validate("255.255.255.255") == True
  assert validate("0.0.0.0") == True
  assert validate("192.168.1.100") == True


def test_out_of_range_octets():
  # Test numbers > 255 in EVERY octet position (CS50 checks for this!)
  assert validate("256.0.0.1") == False
  assert validate("0.256.0.1") == False
  assert validate("0.0.256.1") == False
  assert validate("0.0.0.256") == False
  assert validate("512.512.512.512") == False
  assert validate("1.2.3.1000") == False


def test_invalid_formats():
  assert validate("cat") == False
  assert validate("192.168.1") == False
  assert validate("192.168.1.1.1") == False
  assert validate("192.168.1.") == False
  assert validate("192.168.01.1") == False
  assert validate("192.168.1.-1") == False
