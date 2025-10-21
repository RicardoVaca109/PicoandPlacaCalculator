from services.pico_and_placa_validators import (
    validate_weekday,
    validate_hour,
    validate_plate_by_day,
)


def check_pico_placa(
    vehicle_plate: str, calculate_date: str, calculate_hour: str
) -> str:
    if validate_weekday(calculate_date):
        if validate_hour(calculate_hour):
            if validate_plate_by_day(vehicle_plate, calculate_date):
                return (
                    "Tienes Pico y Placa | Fecha: {} | Placa {} | Hora: {}<br>"
                    "You have Pico and Placa | Date: {} | Plate {} | Hour: {}"
                ).format(
                    calculate_date, vehicle_plate, calculate_hour,
                    calculate_date, vehicle_plate, calculate_hour
                )
            else:
                return (
                    "No Pico y Placa (Por Placa)| Fecha: {} | Placa{} |Hora: {}<br>"
                    "No Pico and Placa (Cause: Plate) | Date: {} | Plate {} | Hour: {}"
                ).format(
                    calculate_date, vehicle_plate, calculate_hour,
                    calculate_date, vehicle_plate, calculate_hour
                )
        else:
            return (
                "No Pico y Placa (Por Hora) | Fecha: {} | Placa {} | Hora: {}<br>"
                "N Pico and Placa (Cause: Hour) | Date: {} | Plate {} | Hour: {}"
            ).format(
                calculate_date, vehicle_plate, calculate_hour,
                calculate_date, vehicle_plate, calculate_hour
            )
    else:
        return (
            "No tienes Pico y Placa<br>"
            "You don't have Pico and Placa"
        )
