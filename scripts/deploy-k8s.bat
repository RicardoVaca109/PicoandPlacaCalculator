# Script para desplegar la aplicación con ArgoCD
# Ejecutar desde el directorio raíz del proyecto

echo "=== Configuración de Pico y Placa Calculator en Kubernetes ==="
echo.

echo "[1/5] Verificando que minikube esté corriendo..."
minikube status
if %errorlevel% neq 0 (
    echo Error: Minikube no está corriendo. Iniciando...
    minikube start
)
echo.

echo "[2/5] Creando secret de LaunchDarkly..."
echo IMPORTANTE: Edita k8s/secret.yaml con tu SDK Key real antes de continuar
pause
kubectl apply -f k8s\secret.yaml
echo.

echo "[3/5] Desplegando aplicación con ArgoCD..."
kubectl apply -f argocd\application.yaml
echo.

echo "[4/5] Esperando sincronización de ArgoCD..."
timeout /t 10
kubectl get applications -n argocd
echo.

echo "[5/5] Verificando recursos desplegados..."
kubectl get deployments
kubectl get services
kubectl get pods
echo.

echo "=== Deployment completado ==="
echo.
echo "Para acceder a la aplicación:"
echo "  minikube service pico-placa-service"
echo.
echo "Para ver ArgoCD dashboard:"
echo "  kubectl port-forward svc/argocd-server -n argocd 8080:443"
echo "  Luego visita: https://localhost:8080"
echo.
echo "Para obtener password de ArgoCD:"
echo "  kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath={.data.password}"
echo.
