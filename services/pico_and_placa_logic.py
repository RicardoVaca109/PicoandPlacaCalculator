from services.pico_and_placa_validators import validate_weekday,validate_hour,validate_plate_by_day

def check_pico_placa(vehicle_plate: str, calculate_date: str, calculate_hour: str) -> str:
        if validate_weekday(calculate_date):
            if validate_hour(calculate_hour):
                if validate_plate_by_day(vehicle_plate,calculate_date ):
                    return(f"Tienes Pico y Placa | Fecha: {calculate_date} |Placa {vehicle_plate} |  Hora: {calculate_hour}<br>" 
                              f"You have Pico and Placa | Date: {calculate_date} |Plate {vehicle_plate} |  Hour: {calculate_hour}"
                        )
                else:
                    return(f"No tienes Pico y Placa (Por Placa) |Fecha: {calculate_date}| Placa {vehicle_plate} | Hora: {calculate_hour}<br>"
                              f"You don't have Pico and Placa (Cause: Plate) |Date: {calculate_date}| Plate {vehicle_plate} | Hour: {calculate_hour}" 
                        )
            else:
                return(f"No tienes Pico y Placa (Por Hora) | Fecha: {calculate_date}|  Placa {vehicle_plate} |  Hora: {calculate_hour}<br>"
                          f"You don't have Pico and Placa (Cause: Hour) |  Date: {calculate_date}|  Plate {vehicle_plate} |  Hour: {calculate_hour}" 
                    )
        else:
            return(f"No tienes Pico y Placa<br>"
                      f"You don't have Pico and Placa"
                )