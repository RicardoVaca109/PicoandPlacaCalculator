# 🚀 Acceso a ArgoCD Dashboard

## Credenciales de Acceso

**URL:** https://localhost:8081

**Usuario:** `admin`

**Contraseña:** `1dNXpOTEcts32wXz`

---

## Pasos para Acceder

### 1. Iniciar Port-Forward

```bash
kubectl port-forward svc/argocd-server -n argocd 8081:443
```

Deja esta terminal abierta mientras trabajas con ArgoCD.

### 2. Abrir Navegador

Accede a: **https://localhost:8081**

⚠️ **Nota:** El navegador mostrará una advertencia de seguridad porque usa un certificado autofirmado. Esto es normal, haz clic en "Avanzado" y luego "Continuar al sitio".

### 3. Login

- **Username:** `admin`
- **Password:** `1dNXpOTEcts32wXz`

---

## 🔍 Verificar la Aplicación en ArgoCD

Una vez dentro del dashboard:

1. Deberías ver la aplicación **`pico-placa-app`**
2. Verifica el estado:
   - **Sync Status:** Debe mostrar "Synced" (sincronizado)
   - **Health Status:** Debe mostrar "Healthy" (saludable)

### Si aparece error "app path does not exist":

Esto significa que ArgoCD no puede encontrar la carpeta `k8s` en el repositorio. Vamos a solucionarlo:

#### Opción 1: Refresh Manual desde UI
1. Haz clic en la aplicación `pico-placa-app`
2. Haz clic en el botón "REFRESH"
3. Espera unos segundos

#### Opción 2: Eliminar y Recrear
```bash
# Eliminar la aplicación
kubectl delete application pico-placa-app -n argocd

# Esperar 5 segundos
timeout /t 5

# Recrear
kubectl apply -f argocd\application.yaml
```

---

## 📊 Monitorear el Despliegue

### Ver Pods Desplegados
```bash
kubectl get pods
```

Deberías ver:
```
NAME                              READY   STATUS    RESTARTS   AGE
pico-placa-app-xxxxxxxxxx-xxxxx   1/1     Running   0          1m
pico-placa-app-xxxxxxxxxx-xxxxx   1/1     Running   0          1m
```

### Ver Services
```bash
kubectl get svc
```

Deberías ver:
```
NAME                  TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
pico-placa-service    NodePort   10.96.xxx.xxx   <none>        80:30080/TCP   1m
```

### Ver Logs de la Aplicación
```bash
kubectl logs -l app=pico-placa
```

Deberías ver:
```
✅ LaunchDarkly SDK initialized successfully
```

---

## 🌐 Acceder a la Aplicación

```bash
minikube service pico-placa-service
```

Esto abrirá automáticamente tu navegador con la URL correcta.

O manualmente:
```bash
minikube service pico-placa-service --url
```

---

## 🧪 Probar Feature Flags

### 1. Accede a LaunchDarkly Dashboard
https://app.launchdarkly.com

### 2. Crea los Feature Flags

#### Flag: `enhanced-ui`
- **Type:** Boolean
- **Default:** OFF
- **Descripción:** "Activar interfaz mejorada con gradientes y Bootstrap icons"

#### Flag: `optimized-calculation`
- **Type:** Boolean
- **Default:** OFF
- **Descripción:** "Activar mensajes optimizados con emojis"

### 3. Prueba el Flag `enhanced-ui`

**Con flag OFF:**
- Interfaz simple, fondo gris
- Título normal "Pico y Placa Calculator"

**Con flag ON:**
- Interfaz con gradiente morado
- Iconos de Bootstrap
- Badge "Enhanced UI Enabled"
- Diseño moderno

### 4. Prueba el Flag `optimized-calculation`

**Con flag OFF:**
- Mensajes simples: "Tienes Pico y Placa"

**Con flag ON:**
- Mensajes con emojis: "✅ Libre de Pico y Placa"
- "❌ RESTRICCIÓN ACTIVA"
- Formato mejorado con iconos

---

## 🔄 Sincronización Automática de ArgoCD

ArgoCD está configurado con:

✅ **Auto-Sync:** Los cambios en GitHub se despliegan automáticamente
✅ **Self-Heal:** Si alguien modifica los recursos manualmente, ArgoCD los revierte
✅ **Prune:** Elimina recursos que ya no están en Git

### Probar Auto-Sync

1. Modifica `k8s/deployment.yaml` (ej: cambiar replicas a 3)
2. Haz commit y push
3. En 1-2 minutos, ArgoCD detectará el cambio
4. Verás el nuevo deployment en el dashboard
5. Verifica: `kubectl get pods` (deberías ver 3 pods)

---

## 🛠️ Comandos Útiles

### Ver estado de ArgoCD
```bash
kubectl get applications -n argocd
```

### Ver detalles de la app
```bash
kubectl describe application pico-placa-app -n argocd
```

### Forzar sincronización (desde CLI)
```bash
# Instalar ArgoCD CLI primero
# https://argo-cd.readthedocs.io/en/stable/cli_installation/

argocd app sync pico-placa-app
```

### Ver historial de despliegues
```bash
argocd app history pico-placa-app
```

### Rollback a versión anterior
```bash
argocd app rollback pico-placa-app <revision-number>
```

---

## ❌ Troubleshooting

### Error: "app path does not exist"

**Problema:** ArgoCD no encuentra la carpeta `k8s` en GitHub.

**Solución:**
1. Verifica que hiciste push: `git log --oneline -5`
2. Verifica en GitHub que existe la carpeta `k8s`
3. Intenta refresh manual en el dashboard

### Pods no inician

**Problema:** Pods en estado `ImagePullBackOff` o `ErrImagePull`

**Solución:**
1. Verifica que la imagen existe: La imagen debe estar en Docker Hub
2. Por ahora, usa una imagen de prueba:

```bash
# Editar deployment.yaml y cambiar la imagen a:
image: nginx:latest
```

3. Aplica cambios y push

### LaunchDarkly no se conecta

**Problema:** SDK no se inicializa

**Solución:**
1. Verifica el secret: `kubectl get secret launchdarkly-secret -o yaml`
2. Verifica que el SDK Key es correcto
3. Ve los logs: `kubectl logs -l app=pico-placa`

---

## 📝 Resumen de URLs

| Servicio | URL | Credenciales |
|----------|-----|--------------|
| ArgoCD Dashboard | https://localhost:8081 | admin / 1dNXpOTEcts32wXz |
| LaunchDarkly | https://app.launchdarkly.com | Tu cuenta |
| Aplicación | `minikube service pico-placa-service --url` | - |
| GitHub Repo | https://github.com/RicardoVaca109/PicoandPlacaCalculator | - |

---

**Fecha:** Diciembre 2025  
**Proyecto:** Pico y Placa Calculator con ArgoCD + LaunchDarkly
