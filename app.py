from flask import Flask
from ld_client import check_flag
from controllers.main_calculator_controller import main_controller

# Flask app initialization
app = Flask(__name__)

# Register controller Blueprint
app.register_blueprint(main_controller)

@app.route("/feature")
def feature():
    if check_flag("nueva-funcionalidad"):
        return "Feature ACTIVADA"
    else:
        return "Feature DESACTIVADA"

# Main function
if __name__ == "__main__":
    app.run(debug=True)
