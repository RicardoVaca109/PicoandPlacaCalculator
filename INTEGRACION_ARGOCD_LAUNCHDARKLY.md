# Integración ArgoCD y LaunchDarkly - Pico y Placa Calculator

## 📋 Resumen del Proyecto

Este documento describe la integración de **ArgoCD** y **LaunchDarkly** en el proyecto Pico y Placa Calculator, implementando prácticas DevOps modernas para despliegue continuo y gestión de feature flags.

---

## 🚀 Componentes Implementados

### 1. ArgoCD - GitOps y Despliegue Continuo

ArgoCD se ha integrado para automatizar el despliegue de la aplicación en Kubernetes (Minikube).

**Características implementadas:**

- ✅ Sincronización automática desde Git
- ✅ Self-healing (auto-reparación)
- ✅ Monitoreo del estado de los recursos
- ✅ Rollback automático en caso de fallos
- ✅ Prune automático de recursos obsoletos

**Archivos creados:**

- `argocd/application.yaml` - Definición de la Application de ArgoCD
- `k8s/deployment.yaml` - Deployment de Kubernetes
- `k8s/service.yaml` - Service de tipo NodePort
- `k8s/secret.yaml` - Secret para LaunchDarkly SDK Key

---

### 2. LaunchDarkly - Feature Flags

Se ha integrado LaunchDarkly Python SDK para gestionar características mediante feature flags.

**Feature Flags implementados:**

#### Flag 1: `enhanced-ui`

- **Tipo:** Boolean
- **Propósito:** Activar/desactivar interfaz de usuario mejorada
- **Uso:** Mejoras visuales en la página principal

#### Flag 2: `optimized-calculation`

- **Tipo:** Boolean
- **Propósito:** Activar nueva lógica optimizada de cálculo
- **Uso:** Mensajes mejorados con emojis y mejor UX

**Archivos modificados:**

- `app.py` - Inicialización del cliente LaunchDarkly
- `controllers/main_calculator_controller.py` - Uso de feature flags
- `services/pico_and_placa_logic.py` - Lógica optimizada condicional
- `requirements.txt` - Añadido `launchdarkly-server-sdk`

---

### 3. Pipeline CI/CD Mejorado

El Jenkinsfile ha sido actualizado para incluir:

**Nuevas etapas:**

1. **Build Docker Image** - Construcción de imagen Docker
2. **Push Docker Image** - Subida a Docker Hub
3. Mantiene las etapas anteriores: Checkout, Setup, Lint, Tests, Deploy

**Variables de entorno añadidas:**

```groovy
DOCKER_IMAGE = "ricardovaca109/pico-placa"
DOCKER_CREDENTIALS_ID = "docker_hub_credentials"
```

---

## 📊 Estrategia de Despliegue Implementada

### **Dark Launch (Lanzamiento Oscuro)**

La estrategia principal implementada es **Dark Launch**, complementada con elementos de **Canary Release**.

#### ¿Por qué Dark Launch?

**Definición:**
Dark Launch es una técnica donde el nuevo código se despliega en producción pero permanece "invisible" para los usuarios hasta que se activa mediante feature flags.

**Implementación en nuestro proyecto:**

1. **Despliegue Silencioso:**

   - La nueva lógica optimizada (`check_pico_placa_optimized`) está desplegada en producción
   - Por defecto, el flag `optimized-calculation` está en `false`
   - Los usuarios continúan viendo la versión antigua

2. **Activación Controlada:**

   ```python
   use_new_logic = ld_client.variation("optimized-calculation", user, False)
   ```

   - Podemos activar la nueva funcionalidad sin redesplegar
   - Control granular por usuario o porcentaje

3. **Rollback Instantáneo:**
   - Si hay problemas, desactivamos el flag en LaunchDarkly
   - No requiere rollback de código
   - Cambio en segundos, no minutos

#### Ventajas de esta estrategia:

✅ **Riesgo Minimizado:** Nueva funcionalidad probada en producción sin impacto
✅ **Testing en Producción:** Validación con datos reales
✅ **Rollback Instantáneo:** Sin necesidad de redesplegar
✅ **Despliegue Gradual:** Activación progresiva por porcentajes
✅ **A/B Testing Posible:** Comparar versiones con usuarios reales

---

## 🔄 Flujo de Trabajo DevOps

```
Desarrollador → Git Push → Jenkins Pipeline
                              ↓
                      [Build & Test]
                              ↓
                      [Build Docker Image]
                              ↓
                      [Push to Docker Hub]
                              ↓
                         Git Commit
                              ↓
                    ArgoCD (Auto-Sync)
                              ↓
                    Kubernetes Cluster
                              ↓
                    LaunchDarkly Control
                              ↓
                    Feature Activation
```

---

## 🛠️ Configuración Requerida

### Prerequisitos:

1. ✅ Minikube instalado y corriendo
2. ✅ ArgoCD instalado en el cluster
3. 🔲 Cuenta en LaunchDarkly (obtener SDK Key)
4. 🔲 Cuenta en Docker Hub (para almacenar imágenes)

### Pasos de Implementación:

#### 1. Configurar LaunchDarkly Secret

```bash
# Editar el archivo k8s/secret.yaml con tu SDK Key real
kubectl apply -f k8s/secret.yaml
```

#### 2. Crear Feature Flags en LaunchDarkly

En el dashboard de LaunchDarkly:

- Crear flag: `enhanced-ui` (Boolean, default: false)
- Crear flag: `optimized-calculation` (Boolean, default: false)

#### 3. Configurar Credenciales en Jenkins

```
- docker_hub_credentials: Username + Password de Docker Hub
- github_token: Personal Access Token de GitHub
```

#### 4. Desplegar Application en ArgoCD

```bash
kubectl apply -f argocd/application.yaml
```

#### 5. Verificar ArgoCD

```bash
# Ver aplicaciones
kubectl get applications -n argocd

# Ver sincronización
kubectl describe application pico-placa-app -n argocd
```

---

## 📈 Monitoreo y Observabilidad

### ArgoCD Dashboard

```bash
# Port-forward para acceder al dashboard
kubectl port-forward svc/argocd-server -n argocd 8080:443

# Obtener password inicial
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

Acceder a: https://localhost:8080

- Usuario: `admin`
- Password: (del comando anterior)

### Verificar Despliegue

```bash
# Ver pods
kubectl get pods

# Ver services
kubectl get svc

# Acceder a la aplicación
minikube service pico-placa-service
```

---

## 🧪 Testing de Feature Flags

### Escenario 1: Activación Gradual (10% de usuarios)

```python
# En LaunchDarkly Dashboard:
# 1. Ir a flag "optimized-calculation"
# 2. Configurar rollout: 10% ON, 90% OFF
# 3. Guardar cambios
```

### Escenario 2: Activación por Usuario Específico

```python
# Modificar el user context en el código:
user = {
    "key": request.remote_addr,  # IP del usuario
    "email": "test@example.com"
}

# En LaunchDarkly:
# 1. Agregar regla por email
# 2. test@example.com → True
```

---

## 🎯 Conclusiones

### Estrategia de Despliegue: **Dark Launch**

**Justificación:**

1. **Seguridad:** Desplegamos código nuevo sin riesgo inmediato
2. **Flexibilidad:** Control total sobre cuándo y cómo activar features
3. **Validación:** Probamos en producción con usuarios reales
4. **Reversibilidad:** Rollback instantáneo sin downtime

**Elementos de Canary Release:**

- Activación progresiva (10%, 25%, 50%, 100%)
- Monitoreo de métricas antes de incrementar porcentaje
- Validación automática de health checks

**Diferencia con otras estrategias:**

| Estrategia         | Nuestro Proyecto | Razón                                   |
| ------------------ | ---------------- | --------------------------------------- |
| **Blue/Green**     | ❌ No            | Requiere doble infraestructura          |
| **Rolling Update** | ✅ Parcial       | Kubernetes lo hace automáticamente      |
| **Canary Release** | ✅ Sí            | LaunchDarkly permite rollout gradual    |
| **Dark Launch**    | ✅✅ Principal   | Feature flags controlan visibilidad     |
| **A/B Testing**    | ✅ Posible       | LaunchDarkly permite comparar versiones |

---

## 📚 Recursos y Referencias

- [ArgoCD Documentation](https://argo-cd.readthedocs.io/)
- [LaunchDarkly Python SDK](https://docs.launchdarkly.com/sdk/server-side/python)
- [Feature Flags Best Practices](https://launchdarkly.com/blog/feature-flag-best-practices/)
- [Dark Launch Pattern](https://martinfowler.com/bliki/DarkLaunching.html)

---

## 👥 Equipo

- Proyecto: Pico y Placa Calculator
- Repositorio: https://github.com/RicardoVaca109/PicoandPlacaCalculator
- Curso: DevOps - CI/CD con ArgoCD y Feature Flags

---

**Fecha:** Diciembre 2025  
**Versión:** 2.0 - ArgoCD + LaunchDarkly Integration
