# 🩺 Diagnóstico de Onboarding: {{PROJECT_NAME}}

- **Fecha y Hora:** {{TIMESTAMP}}
- **Ruta del Proyecto:** `{{PROJECT_PATH}}`
- **Estado General:** {{OVERALL_STATUS_BADGE}}

---

## 📊 Resumen Ejecutivo

| Categoría | Estado | Pasados | Advertencias | Fallos |
| :--- | :---: | :---: | :---: | :---: |
| **Runtimes & CLI** | {{RUNTIMES_STATUS}} | {{RUNTIMES_PASS}} | {{RUNTIMES_WARN}} | {{RUNTIMES_FAIL}} |
| **Variables de Entorno** | {{ENV_STATUS}} | {{ENV_PASS}} | {{ENV_WARN}} | {{ENV_FAIL}} |
| **Puertos de Red** | {{PORTS_STATUS}} | {{PORTS_PASS}} | {{PORTS_WARN}} | {{PORTS_FAIL}} |
| **Dependencias del Proyecto** | {{DEPS_STATUS}} | {{DEPS_PASS}} | {{DEPS_WARN}} | {{DEPS_FAIL}} |

---

## 🔍 Detalle de Verificaciones

### 1. Runtimes y Herramientas del Sistema
{{RUNTIMES_DETAILS}}

### 2. Variables de Entorno (`.env`)
{{ENV_DETAILS}}

### 3. Puertos de Red
{{PORTS_DETAILS}}

### 4. Instalación de Dependencias
{{DEPS_DETAILS}}

---

## 🛠️ Plan de Remediación Inmediata

{{REMEDIATION_COMMANDS}}

> [!NOTE]
> Para explicaciones detalladas sobre cómo solucionar cada problema detectado, consulta la guía en:
> [troubleshooting_playbook.md](./references/troubleshooting_playbook.md)
