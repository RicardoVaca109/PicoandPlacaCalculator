from flask import Blueprint, render_template, request
from services.pico_and_placa_validators import validate_weekday,validate_hour,validate_plate_by_day

# Register the controller as a Blueprint
main_controller = Blueprint("main_controller", __name__)


# Route of the HMTL index template
@main_controller.route("/")
def main_page():
    return render_template("index.html")

# Route that manages the User input with the defined functions and logic
@main_controller.route("/post_values", methods = ['POST'])
def obtain_values():
    if request.method == 'POST':
        vehicle_plate = request.form['vehicle_plate']
        calculate_date = request.form['calculate_date']
        calculate_hour = request.form['calculate_hour']
        
                
        if validate_weekday(calculate_date):
            if validate_hour(calculate_hour):
                if validate_plate_by_day(vehicle_plate,calculate_date ):
                    result = (f"Tienes Pico y Placa | Fecha: {calculate_date} |Placa {vehicle_plate} |  Hora: {calculate_hour}<br>" 
                              f"You have Pico and Placa | Date: {calculate_date} |Plate {vehicle_plate} |  Hour: {calculate_hour}"
                            )
                else:
                    result = (f"No tienes Pico y Placa (Por Placa) |Fecha: {calculate_date}| Placa {vehicle_plate} | Hora: {calculate_hour}<br>"
                              f"You don't have Pico and Placa (Cause: Plate) |Date: {calculate_date}| Plate {vehicle_plate} | Hour: {calculate_hour}" 
                            )
            else:
                result = (f"No tienes Pico y Placa (Por Hora) | Fecha: {calculate_date}|  Placa {vehicle_plate} |  Hora: {calculate_hour}<br>"
                          f"You don't have Pico and Placa (Cause: Hour) |  Date: {calculate_date}|  Plate {vehicle_plate} |  Hour: {calculate_hour}" 
                        )
        else:
            result = (f"No tienes Pico y Placa<br>"
                      f"You don't have Pico and Placa"
                    )
        
    return render_template('index.html', message = result)
