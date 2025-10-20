#!/bin/bash
set -euo pipefail

# === CONFIGURACIÓN LOCAL ===
# Usuario de Jenkins
REMOTE_USER=${REMOTE_USER:-ricardo_vaca}

# Host local
REMOTE_HOST=${REMOTE_HOST:-localhost}

# Ruta donde se desplegará la app (ajústala si quieres otro directorio)
REMOTE_PATH=${REMOTE_PATH:-/home/ricardo_vaca/app}

# Carpeta local del proyecto (el workspace de Jenkins)
LOCAL_BUILD_PATH=${LOCAL_BUILD_PATH:-./}

echo "====================================================="
echo " Desplegando aplicación Flask en entorno local"
echo " Origen: ${LOCAL_BUILD_PATH}"
echo " Destino: ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_PATH}"
echo "====================================================="

# Crear la carpeta destino si no existe
mkdir -p ${REMOTE_PATH}

# Sincronizar archivos (simula deploy)
rsync -avz --delete --exclude '.git' --exclude '.venv' ${LOCAL_BUILD_PATH} ${REMOTE_PATH}

echo "Despliegue completado con éxito 🚀"
echo "La aplicación está lista en ${REMOTE_PATH}"
