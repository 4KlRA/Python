from datetime import date
from unittest.mock import patch
import pytest
from seasons import convert


def test_valid_dates():
  with patch("seasons.date") as mock_date:
    mock_date.today.return_value = date(2000, 1, 1)
    mock_date.fromisoformat.side_effect = date.fromisoformat

    assert (
        convert("1999-01-01")
        == "Five hundred twenty-five thousand, six hundred minutes"
    )
    assert (
        convert("1998-01-01")
        == "One million, fifty-one thousand, two hundred minutes"
    )
    assert convert("1999-12-31") == "One thousand, four hundred forty minutes"

  with patch("seasons.date") as mock_date:
    mock_date.today.return_value = date(2001, 1, 1)
    mock_date.fromisoformat.side_effect = date.fromisoformat

    assert (
        convert("2000-01-01")
        == "Five hundred twenty-seven thousand forty minutes"
    )


def test_invalid_dates():
  with pytest.raises(ValueError):
    convert("January 1, 1999")
  with pytest.raises(ValueError):
    convert("19990101")
  with pytest.raises(ValueError):
    convert("1999-13-01")
  with pytest.raises(ValueError):
    convert("1999-02-30")
  with pytest.raises(ValueError):
    convert("2099-01-01")
