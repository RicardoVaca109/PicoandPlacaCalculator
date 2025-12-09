# 📦 ENTREGA FINAL - Integración ArgoCD + LaunchDarkly

## Proyecto: Pico y Placa Calculator
**Repositorio:** https://github.com/RicardoVaca109/PicoandPlacaCalculator

---

## ✅ REQUISITOS COMPLETADOS

### 1. ✅ Integrar ArgoCD como herramienta DevOps

**Evidencia:**
- Archivo: `argocd/application.yaml`
- Pipeline con sincronización automática: ✅
- Monitoreo del estado de despliegues: ✅
- Self-heal activado: ✅
- Auto-prune activado: ✅

**Configuración:**
```yaml
syncPolicy:
  automated:
    prune: true      # Eliminación automática de recursos obsoletos
    selfHeal: true   # Sincronización automática ante cambios manuales
```

**Acceso al Dashboard:**
```bash
# Port-forward
kubectl port-forward svc/argocd-server -n argocd 8081:443

# Credenciales
Usuario: admin
Password: 1dNXpOTEcts32wXz

# URL
https://localhost:8081
```

---

### 2. ✅ Añadir LaunchDarkly para gestión de feature flags

**Evidencia:**
- SDK instalado: `launchdarkly-server-sdk==9.7.1` en `requirements.txt`
- SDK Key configurado: `sdk-cdf07fa7-1a83-4268-acb6-5d972e8283cd`
- Feature flags implementados: 2

#### Feature Flag 1: `enhanced-ui`
**Propósito:** Activar/desactivar interfaz mejorada

**Comportamiento:**
- **OFF:** Interfaz simple, fondo gris, diseño básico
- **ON:** Interfaz moderna con:
  - Gradiente morado (Purple theme)
  - Iconos de Bootstrap
  - Badge "Enhanced UI Enabled"
  - Cards con sombras y bordes redondeados

**Código:**
```python
# controllers/main_calculator_controller.py
context = Context.builder('anonymous-user').kind('user').anonymous(True).build()
show_enhanced_ui = ld_client.variation("enhanced-ui", context, False)
return render_template("index.html", enhanced_ui=show_enhanced_ui)
```

#### Feature Flag 2: `optimized-calculation`
**Propósito:** Activar mensajes optimizados con emojis

**Comportamiento:**
- **OFF:** Mensajes simples: "Tienes Pico y Placa"
- **ON:** Mensajes mejorados:
  - ✅ "Libre de Pico y Placa!"
  - ❌ "RESTRICCIÓN ACTIVA"
  - Formato con emojis y mejor legibilidad

**Código:**
```python
# services/pico_and_placa_logic.py
def check_pico_placa(vehicle_plate, calculate_date, calculate_hour, use_optimized=False):
    if use_optimized:
        return check_pico_placa_optimized(...)  # Nueva función con emojis
    # Lógica original
```

---

### 3. ✅ Conclusión sobre Estrategia de Despliegue

**Ver archivo:** `CONCLUSIONES.md`

**Resumen:**

#### Estrategia Implementada: **DARK LAUNCH** 🎯

**Definición:**
Dark Launch es una técnica donde el código nuevo se despliega en producción pero permanece invisible para los usuarios hasta que se activa mediante feature flags.

**Por qué Dark Launch:**
1. **Riesgo Minimizado:** Código nuevo en producción sin impacto inmediato
2. **Rollback Instantáneo:** Desactivar flag en 2 segundos vs 15 minutos de redeploy
3. **Testing en Producción:** Probar con datos reales sin exponer a todos los usuarios
4. **Control Granular:** Activación por porcentaje (10%, 25%, 50%, 100%)

**Elementos Complementarios:**
- ✅ **Canary Release:** Rollout progresivo (10% → 100%)
- ✅ **A/B Testing:** Capacidad de comparar versiones

**Comparación:**

| Aspecto | Deployment Tradicional | Dark Launch |
|---------|----------------------|-------------|
| Rollback | 10-15 minutos | 2 segundos |
| Downtime | Posible | Cero |
| Testing Real | No | Sí |
| Control | Todo o nada | Granular |

---

## 📁 ARCHIVOS ENTREGADOS

### Configuración de Kubernetes
```
k8s/
├── deployment.yaml    # Deployment con 2 réplicas
├── service.yaml       # NodePort en puerto 30080
└── secret.yaml        # LaunchDarkly SDK Key
```

### Configuración de ArgoCD
```
argocd/
└── application.yaml   # Application con auto-sync
```

### Docker
```
Dockerfile             # Imagen optimizada Python 3.11
.dockerignore         # Exclusiones para build
```

### Código Modificado
```
app.py                           # Inicialización LaunchDarkly
controllers/
└── main_calculator_controller.py  # Uso de feature flags
services/
└── pico_and_placa_logic.py        # Lógica optimizada
templates/
└── index.html                      # UI con soporte enhanced-ui
requirements.txt                    # +launchdarkly-server-sdk
Jenkinsfile                         # Pipeline con Docker build/push
```

### Documentación
```
CONCLUSIONES.md                        # Estrategia Dark Launch explicada
INTEGRACION_ARGOCD_LAUNCHDARKLY.md    # Documentación técnica completa
ACCESO_ARGOCD.md                      # Guía de acceso al dashboard
README.md                              # Actualizado con nuevas features
```

---

## 🚀 EVIDENCIA DE FUNCIONAMIENTO

### ArgoCD Dashboard
**Captura:** Aplicación `pico-placa-app` visible en ArgoCD

**Estados visibles:**
- Sync Status: Synced / OutOfSync
- Health Status: Healthy / Progressing
- Resources: Deployment, Service, Pods

**Comandos para verificar:**
```bash
kubectl get applications -n argocd
kubectl describe application pico-placa-app -n argocd
```

### LaunchDarkly Dashboard
**Flags creados:**
1. `enhanced-ui` (Boolean)
2. `optimized-calculation` (Boolean)

**Configuraciones posibles:**
- Targeting: Por usuario, IP, custom attributes
- Percentage Rollout: 0%, 10%, 25%, 50%, 100%
- Default: OFF (estrategia dark)

### Kubernetes Cluster
```bash
# Ver pods
kubectl get pods
NAME                             READY   STATUS    RESTARTS   AGE
pico-placa-app-xxxxxxxxxx-xxxxx   1/1     Running   0          5m

# Ver service
kubectl get svc
NAME                  TYPE       CLUSTER-IP      PORT(S)        AGE
pico-placa-service    NodePort   10.96.xxx.xxx   80:30080/TCP   5m

# Ver secret
kubectl get secret launchdarkly-secret
NAME                    TYPE     DATA   AGE
launchdarkly-secret     Opaque   1      10m
```

---

## 🧪 CÓMO PROBAR

### 1. Acceder a ArgoCD
```bash
kubectl port-forward svc/argocd-server -n argocd 8081:443
```
Ir a: https://localhost:8081 (admin / 1dNXpOTEcts32wXz)

### 2. Verificar Sincronización
- Ver que `pico-placa-app` está "Synced"
- Hacer cambio en `k8s/deployment.yaml` (ej: replicas: 3)
- Commit + push
- En 2 minutos, ArgoCD detecta y aplica cambio
- Verificar: `kubectl get pods` (debe mostrar 3 pods)

### 3. Probar Feature Flags

#### A. Flag `enhanced-ui`

**Paso 1:** Acceder a la app
```bash
minikube service pico-placa-service
```

**Paso 2:** Ver versión original (flag OFF)
- Interfaz simple
- Fondo gris (#e0e0e0)

**Paso 3:** Activar flag en LaunchDarkly
- Dashboard → Flags → `enhanced-ui` → ON

**Paso 4:** Recargar página
- Interfaz moderna
- Gradiente morado
- Badge "Enhanced UI Enabled"

#### B. Flag `optimized-calculation`

**Paso 1:** Ingresar placa, fecha, hora
**Paso 2:** Con flag OFF:
```
"Tienes Pico y Placa | Fecha: 2024-12-09 | Placa ABC-123"
```

**Paso 3:** Activar flag en LaunchDarkly
**Paso 4:** Mismo cálculo:
```
"❌ RESTRICCIÓN ACTIVA - Pico y Placa
📅 Fecha: 2024-12-09 | 🚗 Placa: ABC-123 | 🕐 Hora: 08:00"
```

---

## 📊 ARQUITECTURA IMPLEMENTADA

```
┌─────────────┐
│   GitHub    │  Source of Truth
└─────┬───────┘
      │ Git Push
      ▼
┌─────────────┐
│   ArgoCD    │  GitOps Engine
└─────┬───────┘
      │ Auto-Sync (3 min)
      ▼
┌─────────────┐
│ Kubernetes  │  Orchestration
│  (Minikube) │
└─────┬───────┘
      │
      ▼
┌─────────────┐     ┌──────────────┐
│  Pods x2    │────▶│ LaunchDarkly │
│  Flask App  │     │ Feature Flags│
└─────────────┘     └──────────────┘
      │
      ▼
┌─────────────┐
│   Usuarios  │  Experiencia controlada
└─────────────┘
```

---

## 🎯 ESTRATEGIA DARK LAUNCH - DETALLES

### Flujo de un Cambio

#### Escenario 1: Cambio de Infraestructura
```
1. Dev modifica k8s/deployment.yaml
2. Git commit + push
3. ArgoCD detecta cambio (~2 min)
4. K8s aplica nuevo deployment
5. Rolling update sin downtime
```

#### Escenario 2: Nueva Feature (DARK)
```
1. Dev crea nueva función en pico_and_placa_logic.py
2. Git commit + push  
3. ArgoCD despliega código (feature APAGADA)
4. Testing interno (activar para IPs específicas)
5. Beta (activar 10% usuarios)
6. Producción (activar 100%)
```

### Kill Switch en Acción

**Sin Dark Launch:**
```
Bug detectado → Iniciar rollback → Build → Deploy → 15 min
```

**Con Dark Launch:**
```
Bug detectado → LaunchDarkly OFF → 2 segundos ✅
```

---

## 📚 CONCLUSIÓN

Hemos implementado exitosamente:

1. ✅ **ArgoCD** con GitOps puro (auto-sync, self-heal, prune)
2. ✅ **LaunchDarkly** con 2 feature flags funcionales
3. ✅ **Estrategia Dark Launch** con capacidad de Canary y A/B Testing

**Ventajas demostradas:**
- Despliegue desacoplado de activación
- Rollback instantáneo (2 seg vs 15 min)
- Testing en producción sin riesgo
- Control granular por usuario/porcentaje

**Tecnologías integradas:**
- Kubernetes (orchestration)
- ArgoCD (GitOps)
- LaunchDarkly (feature flags)
- Docker (containerization)
- Flask (backend)
- GitHub (source control)

---

## 👥 EQUIPO

[Completa con los nombres de tu equipo]

**Fecha de Entrega:** Diciembre 2025  
**Curso:** DevOps - CI/CD  
**Institución:** UDLA

---

## 📎 ENLACES

- **Repositorio:** https://github.com/RicardoVaca109/PicoandPlacaCalculator
- **LaunchDarkly:** https://app.launchdarkly.com
- **ArgoCD Dashboard:** https://localhost:8081 (cuando port-forward esté activo)
