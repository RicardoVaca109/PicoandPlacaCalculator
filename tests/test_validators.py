# tests/test_validators.py
import pytest
from datetime import datetime
from services.pico_and_placa_validators import (
    validate_plate_by_day,
    validate_weekday,
    validate_hour,
)

def test_validate_weekday_true_for_monday():
    assert validate_weekday("2025-10-20")  # Monday (example)

def test_validate_weekday_false_for_sunday():
    assert not validate_weekday("2025-10-19")  # Sunday

@pytest.mark.parametrize("time_str,expected", [
    ("06:00", True),
    ("09:30", True),
    ("07:15", True),
    ("15:59", False),
    ("16:00", True),
    ("20:00", True),
    ("20:01", False),
])
def test_validate_hour(time_str, expected):
    assert validate_hour(time_str) is expected

def test_validate_plate_by_day_matches_rules():
    # Monday restriction digits 1,2 -> choose plate ending with 1
    assert validate_plate_by_day("ABC-1231", "2025-10-20") is True

def test_validate_plate_by_day_non_restricted():
    # Sunday should not be in restrictions (weekend)
    with pytest.raises(ValueError):
        # If plate date conversion fails or logic differs, ensure behavior
        # But our implementation expects a valid date — we test a weekday not in restrictions
        validate_plate_by_day("ABC-1233", "2025-10-19")