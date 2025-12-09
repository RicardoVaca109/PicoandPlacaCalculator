from flask import Flask
from controllers.main_calculator_controller import main_controller
import ldclient
from ldclient import Context
from ldclient.config import Config
import os

# Configuración de LaunchDarkly
SDK_KEY = os.environ.get(
    "LAUNCHDARKLY_SDK_KEY", "sdk-cdf07fa7-1a83-4268-acb6-5d972e8283cd"
)
ldclient.set_config(Config(SDK_KEY))
ld_client = ldclient.get()

# Flask app initialization
app = Flask(__name__)

# Verificar inicialización de LaunchDarkly
if ld_client.is_initialized():
    print("✅ LaunchDarkly SDK initialized successfully")
    # Tracking member ID para onboarding
    tracking_context = (
        Context.builder("onboarding-user")
        .kind("user")
        .set("email", "team@picoplaca.dev")
        .build()
    )
    ld_client.track("6937b393c1b12d0dd20fa20f", tracking_context)
else:
    print("⚠️ LaunchDarkly SDK failed to initialize")

# Hacer el cliente de LaunchDarkly disponible globalmente
app.config["LD_CLIENT"] = ld_client

# Register controller Blueprint
app.register_blueprint(main_controller)

# Main function
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
