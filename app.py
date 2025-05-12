from flask import Flask
from controllers.main_calculator_controller import main_controller

# Flask app initialization
app = Flask(__name__)

# Register controller Blueprint 
app.register_blueprint(main_controller)

# Main function
if __name__ == "__main__":
    app.run(debug=True)