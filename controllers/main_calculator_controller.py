from flask import Blueprint, render_template, request, current_app
from services.pico_and_placa_logic import check_pico_placa
from ldclient import Context

# Register the controller as a Blueprint
main_controller = Blueprint("main_controller", __name__)


# Route of the HMTL index template
@main_controller.route("/")
def main_page():
    # Feature flag: mostrar mensaje de bienvenida mejorado
    ld_client = current_app.config.get("LD_CLIENT")

    # Crear contexto de LaunchDarkly usando el formato moderno
    context = Context.builder("anonymous-user").kind("user").anonymous(True).build()

    show_enhanced_ui = False
    if ld_client and ld_client.is_initialized():
        show_enhanced_ui = ld_client.variation("enhanced-ui", context, False)

    return render_template("index.html", enhanced_ui=show_enhanced_ui)


# Route that manages the User input with the defined functions and logic
@main_controller.route("/post_values", methods=["POST"])
def obtain_values():
    if request.method == "POST":
        vehicle_plate = request.form["vehicle_plate"]
        calculate_date = request.form["calculate_date"]
        calculate_hour = request.form["calculate_hour"]

        # Feature flag: usar nueva lógica de cálculo optimizada
        ld_client = current_app.config.get("LD_CLIENT")

        # Crear contexto con información del usuario
        context = (
            Context.builder(request.remote_addr or "unknown")
            .kind("user")
            .set("plate", vehicle_plate)
            .set("user_agent", request.headers.get("User-Agent", "unknown"))
            .build()
        )

        use_new_logic = False
        if ld_client and ld_client.is_initialized():
            use_new_logic = ld_client.variation("optimized-calculation", context, True)

        result = check_pico_placa(
            vehicle_plate, calculate_date, calculate_hour, use_new_logic
        )

    return render_template("index.html", message=result)
