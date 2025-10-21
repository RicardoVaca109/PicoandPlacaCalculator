# tests/test_logic.py
from services.pico_and_placa_logic import check_pico_placa


def test_check_pico_placa_when_restricted():
    # Monday 2025-10-20 restricted digits 1,2 -> plate ending 1 during restricted hour
    result = check_pico_placa("ABC-1231", "2025-10-20", "07:30")
    assert "Tienes Pico y Placa" in result


def test_check_pico_placa_not_by_hour():
    # Monday but outside restricted hours
    result = check_pico_placa("ABC-1231", "2025-10-20", "10:00")
    assert "No Pico y Placa (Por Hora)" in result


def test_check_pico_placa_not_by_plate():
    # Monday during restricted hours but plate not restricted
    result = check_pico_placa("ABC-1233", "2025-10-20", "07:30")
    assert "No Pico y Placa (Por Placa)" in result


def test_check_pico_placa_weekend():
    # Sunday should be outside restrictions
    result = check_pico_placa("ABC-1231", "2025-10-19", "07:30")
    assert "No tienes Pico y Placa" in result
