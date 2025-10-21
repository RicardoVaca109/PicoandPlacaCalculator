@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

REM === CONFIGURACIÓN LOCAL ===
SET REMOTE_USER=%REMOTE_USER%
SET REMOTE_HOST=%REMOTE_HOST%
SET REMOTE_PATH=%REMOTE_PATH%
SET LOCAL_BUILD_PATH=%WORKSPACE%

echo =====================================================
echo  Desplegando aplicación Flask en entorno local
echo  Origen: !LOCAL_BUILD_PATH!
echo  Destino: !REMOTE_USER!@!REMOTE_HOST!:!REMOTE_PATH!
echo =====================================================

REM Crear carpeta destino
if not exist "!REMOTE_PATH!" mkdir "!REMOTE_PATH!"

REM Crear archivo de exclusiones
echo .git> exclude.txt
echo .venv>> exclude.txt

REM Copiar archivos (simula deploy)
xcopy "!LOCAL_BUILD_PATH!\*" "!REMOTE_PATH!" /E /I /Y /EXCLUDE:exclude.txt

echo Despliegue completado con éxito 🚀
echo La aplicación está lista en !REMOTE_PATH!

REM Limpiar archivo de exclusiones
del exclude.txt
