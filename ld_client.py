import os
import ldclient
from ldclient import Config

# Obtener SDK key desde variable de entorno
sdk_key = os.getenv("LD_SDK_KEY")

# Configurar solo si existe clave
if sdk_key:
    ldclient.set_config(Config(
        sdk_key,
        send_events=True
    ))
    client = ldclient.get()
else:
    client = None


def check_flag(flag_key: str, user_key: str = "default-user"):
    """
    Retorna True/False según el estado del feature flag.
    No lanza excepciones si LaunchDarkly falla.
    """
    if client is None:
        return False

    try:
        user = {"key": user_key}
        return client.variation(flag_key, user, False)
    except Exception:
        return False