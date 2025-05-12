from flask import Blueprint, render_template, request
from services.pico_and_placa_logic import check_pico_placa

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
        
        result = check_pico_placa (vehicle_plate, calculate_date, calculate_hour)
        
    return render_template('index.html', message = result)
