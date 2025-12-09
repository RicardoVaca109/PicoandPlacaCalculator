from services.pico_and_placa_validators import (
    validate_weekday,
    validate_hour,
    validate_plate_by_day,
)


def check_pico_placa(
    vehicle_plate: str,
    calculate_date: str,
    calculate_hour: str,
    use_optimized: bool = False,
) -> str:
    """
    Verifica si un vehículo tiene restricción de Pico y Placa.

    Args:
        vehicle_plate: Placa del vehículo
        calculate_date: Fecha a verificar
        calculate_hour: Hora a verificar
        use_optimized: Flag de LaunchDarkly para usar versión optimizada

    Returns:
        Mensaje con el resultado de la verificación
    """

    if use_optimized:
        # Versión optimizada con mensajes mejorados
        return check_pico_placa_optimized(vehicle_plate, calculate_date, calculate_hour)

    # Versión original
    if validate_weekday(calculate_date):
        if validate_hour(calculate_hour):
            if validate_plate_by_day(vehicle_plate, calculate_date):
                return (
                    "Tienes Pico y Placa | Fecha: {} | Placa {} | Hora: {}<br>"
                    "You have Pico and Placa | Date: {} | Plate {} | Hour: {}"
                ).format(
                    calculate_date,
                    vehicle_plate,
                    calculate_hour,
                    calculate_date,
                    vehicle_plate,
                    calculate_hour,
                )
            else:
                return (
                    "No Pico y Placa (Por Placa)| Fecha: {} | Placa{} |Hora: {}<br>"
                    "No Pico and Placa (Cause: Plate) | Date: {} | Plate {} | Hour: {}"
                ).format(
                    calculate_date,
                    vehicle_plate,
                    calculate_hour,
                    calculate_date,
                    vehicle_plate,
                    calculate_hour,
                )
        else:
            return (
                "No Pico y Placa (Por Hora) | Fecha: {} | Placa {} | Hora: {}<br>"
                "N Pico and Placa (Cause: Hour) | Date: {} | Plate {} | Hour: {}"
            ).format(
                calculate_date,
                vehicle_plate,
                calculate_hour,
                calculate_date,
                vehicle_plate,
                calculate_hour,
            )
    else:
        return "No tienes Pico y Placa<br>" "You don't have Pico and Placa"


def check_pico_placa_optimized(
    vehicle_plate: str, calculate_date: str, calculate_hour: str
) -> str:
    """
    Versión optimizada del cálculo de Pico y Placa con mensajes mejorados.
    Esta es la nueva feature controlada por LaunchDarkly.
    """
    if not validate_weekday(calculate_date):
        return (
            "✅ ¡Libre de Pico y Placa! | Es fin de semana<br>"
            "✅ Free of Pico and Placa! | It's weekend"
        )

    if not validate_hour(calculate_hour):
        return (
            "✅ Puedes circular libremente | Fuera del horario restringido<br>"
            "📅 Fecha: {} | 🚗 Placa: {} | 🕐 Hora: {}<br>"
            "✅ You can drive freely | Outside restricted hours<br>"
            "📅 Date: {} | 🚗 Plate: {} | 🕐 Hour: {}"
        ).format(
            calculate_date,
            vehicle_plate,
            calculate_hour,
            calculate_date,
            vehicle_plate,
            calculate_hour,
        )

    if validate_plate_by_day(vehicle_plate, calculate_date):
        return (
            "❌ RESTRICCIÓN ACTIVA - Pico y Placa<br>"
            "📅 Fecha: {} | 🚗 Placa: {} | 🕐 Hora: {}<br>"
            "⚠️ No puedes circular en este horario<br><br>"
            "❌ ACTIVE RESTRICTION - Pico and Placa<br>"
            "📅 Date: {} | 🚗 Plate: {} | 🕐 Hour: {}<br>"
            "⚠️ You cannot drive at this time"
        ).format(
            calculate_date,
            vehicle_plate,
            calculate_hour,
            calculate_date,
            vehicle_plate,
            calculate_hour,
        )
    else:
        return (
            "✅ Sin restricciones | Tu placa no tiene Pico y Placa hoy<br>"
            "📅 Fecha: {} | 🚗 Placa: {} | 🕐 Hora: {}<br>"
            "✅ No restrictions | Your plate is free today<br>"
            "📅 Date: {} | 🚗 Plate: {} | 🕐 Hour: {}"
        ).format(
            calculate_date,
            vehicle_plate,
            calculate_hour,
            calculate_date,
            vehicle_plate,
            calculate_hour,
        )
