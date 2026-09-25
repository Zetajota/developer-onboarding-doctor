# 🩺 Developer Onboarding Doctor

> **Skill inteligente de diagnóstico, verificación y configuración asistida de entornos de desarrollo local para nuevos miembros de equipo e integración continua.**

[![Skill Standard: Antigravity/Codex](https://img.shields.io/badge/Skill-Antigravity%20%2F%20Codex-blue)](https://github.com)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-green.svg)](https://python.org)
[![Status: Functional](https://img.shields.io/badge/Status-100%25%20Functional-brightgreen)](https://github.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)

---

## 📋 Índice
1. [¿Cuándo y Para Qué Utilizar esta Skill?](#-cuándo-y-para-qué-utilizar-esta-skill)
2. [Estructura del Proyecto y la Skill](#-estructura-del-proyecto-y-la-skill)
3. [Requisitos e Instalación](#-requisitos-e-instalación)
4. [Flujo de Trabajo y Modos de Ejecución](#-flujo-de-trabajo-y-modos-de-ejecución)
5. [Demostración y Casos de Prueba (Éxito vs Errores)](#-demostración-y-casos-de-prueba-éxito-vs-errores)
6. [Decisiones de Diseño y Arquitectura](#-decisiones-de-diseño-y-arquitectura)

---

## 🎯 ¿Cuándo y Para Qué Utilizar esta Skill?

### El Problema
Al clonar un repositorio o incorporarse a un nuevo equipo de desarrollo (*onboarding*), los desarrolladores pierden horas enfrentando problemas silenciosos:
- No tienen la versión correcta de Node.js o Python en su máquina local.
- Les faltan herramientas de consola obligatorias en el `$PATH` (como `git`, `npm` o `docker`).
- Los puertos de red requeridos (ej. `3000`, `5432`, `8080`) ya están ocupados por otros procesos o servidores zombies.
- El archivo `.env` no existe o no tiene las variables de entorno mínimas requeridas respecto a `.env.example`.
- Las carpetas de dependencias (`node_modules`, `.venv`) no fueron instaladas.

### La Solución
**`developer-onboarding-doctor`** automatiza el proceso de diagnóstico de punta a punta:
1. Inspecciona los requisitos del proyecto a través de `onboarding-profile.json` (o los inicializa automáticamente).
2. Evalúa en milisegundos runtimes, versiones SemVer, puertos TCP, variables y dependencias.
3. Emite un semáforo visual inmediato (**🟢 PASS**, **🟡 WARN**, **🔴 FAIL**).
4. Genera comandos de remediación instantánea (`--fix-env`, liberación de puertos) y un informe Markdown enriquecido (`ONBOARDING_DIAGNOSIS.md`).

---

## 📂 Estructura del Proyecto y la Skill

El proyecto cumple estrictamente con el estándar oficial de skills de agentes de inteligencia artificial:

```text
developer-onboarding-doctor/
├── .agents/
│   └── skills/
│       └── developer-onboarding-doctor/
│           ├── SKILL.md                          # Definición formal de la skill con YAML frontmatter y flujo
│           ├── scripts/
│           │   └── doctor.py                     # Motor ejecutable de diagnóstico (Python 3 estándar)
│           ├── assets/
│           │   ├── project_profile_schema.json   # Esquema JSON formal para validar configuraciones
│           │   ├── default_profile.json          # Perfil base reutilizable para inicializar proyectos
│           │   └── report_template.md            # Plantilla Markdown para generar reportes estructurados
│           └── references/
│               ├── troubleshooting_playbook.md   # Manual de resolución paso a paso para cada tipo de error
│               └── environment_standards.md      # Estándares de la industria (Twelve-Factor App Factor III)
├── demo-projects/                                # Proyectos de prueba incluidos para la demostración
│   ├── app-success/                              # Caso 1: Proyecto saludable (Semáforo 🟢 PASS)
│   │   ├── onboarding-profile.json
│   │   ├── .env
│   │   ├── .env.example
│   │   ├── package.json
│   │   └── server.js
│   ├── app-with-issues/                          # Caso 2: Proyecto con fallos habituales (Semáforo 🔴 FAIL)
│   │   ├── onboarding-profile.json
│   │   ├── .env.example                          # Falta .env y dependencias
│   │   └── package.json
│   └── app-corrupted/                            # Caso 3: Manejo de entrada inválida (JSON corrupto)
│       └── onboarding-profile.json
├── tests/
│   └── test_doctor.py                            # Suite de pruebas unitarias automatizadas (unittest)
├── run_demo.sh                                   # Script interactivo para ejecutar la presentación en vivo
└── README.md                                     # Documentación integral del proyecto
```

### Justificación de Archivos:
- **`SKILL.md`**: Es la interfaz que lee el agente inteligente. Contiene las directivas de activación (`description`) y el diagrama de flujo de resolución.
- **`scripts/doctor.py`**: Es el cerebro ejecutable. Desarrollado en Python 3 puro (sin dependencias externas tipo `pip`) para que funcione en cualquier sistema operativo (Linux, macOS, Windows).
- **`assets/project_profile_schema.json`**: Valida que los perfiles sigan un contrato estricto de tipos de datos.
- **`assets/default_profile.json`**: Se utiliza cuando un desarrollador ejecuta `--init` en un proyecto nuevo.
- **`assets/report_template.md`**: Se procesa dinámicamente sustituyendo variables para crear el informe de auditoría.
- **`references/troubleshooting_playbook.md`**: Provee las soluciones técnicas que el agente recomienda al usuario.
- **`references/environment_standards.md`**: Provee el sustento conceptual de por qué se audita cada aspecto.

---

## ⚙️ Requisitos e Instalación

### Requisitos Previos:
- **Python 3.10 o superior** (incluido por defecto en Linux Ubuntu/Debian, macOS y Windows).
- **Bash** (para ejecutar el script automatizado `run_demo.sh`).

### Instalación:
No requiere dependencias de `pip` ni compiladores externos. Únicamente clona el repositorio:

```bash
git clone <URL_DE_TU_REPOSITORIO>
cd developer-onboarding-doctor
chmod +x run_demo.sh .agents/skills/developer-onboarding-doctor/scripts/doctor.py
```

---

## 🚀 Flujo de Trabajo y Modos de Ejecución

### 1. Diagnóstico Básico en Terminal
Para diagnosticar cualquier proyecto local:
```bash
python3 .agents/skills/developer-onboarding-doctor/scripts/doctor.py --project <RUTA_DEL_PROYECTO>
```

### 2. Generación de Reporte Markdown
Para generar un informe formal en el repositorio:
```bash
python3 .agents/skills/developer-onboarding-doctor/scripts/doctor.py --project demo-projects/app-success --report demo-projects/app-success/ONBOARDING_DIAGNOSIS.md
```

### 3. Inicialización Automática de Perfil (`--init`)
Para crear un archivo `onboarding-profile.json` en un proyecto que aún no lo tiene:
```bash
python3 .agents/skills/developer-onboarding-doctor/scripts/doctor.py --project ./mi-nuevo-proyecto --init
```

### 4. Auto-Remediación de Variables de Entorno (`--fix-env`)
Copia de forma segura `.env.example` hacia `.env` sin sobreescribir datos previos:
```bash
python3 .agents/skills/developer-onboarding-doctor/scripts/doctor.py --project demo-projects/app-with-issues --fix-env
```

### 5. Salida en Formato JSON para Pipelines CI/CD (`--json`)
```bash
python3 .agents/skills/developer-onboarding-doctor/scripts/doctor.py --project demo-projects/app-success --json
```

---

## 🧪 Demostración y Casos de Prueba (Éxito vs Errores)

Puedes ejecutar toda la demostración interactiva con un solo comando:
```bash
./run_demo.sh
```

### Caso A: Proyecto Exitoso (`app-success`) — *Happy Path*
- **Entrada:** Proyecto con Node.js compatible, `.env` completo, dependencias y puertos libres.
- **Resultado Esperado:** Código de salida `0` y semáforo `🟢 TODO LISTO (PASS)`.
- **Salida de Ejemplo:**
```text
================================================================
🩺 DEVELOPER ONBOARDING DOCTOR
Proyecto : ecommerce-api-success
Ubicación: /ruta/demo-projects/app-success
Resultado: 🟢 TODO LISTO (PASS)
================================================================

[1] Runtimes y Herramientas del Sistema:
  🟢 node       -> Versión 20.10.0 instalada (Requerida >= 16.0.0).
  🟢 python3    -> Versión 3.11.8 instalada (Requerida >= 3.8.0).
  🟢 CLI:git    -> Disponible en: /usr/bin/git
  🟢 CLI:npm    -> Disponible en: /usr/bin/npm

[2] Variables de Entorno:
  🟢 Variables requeridas -> Todas las variables clave (3) están configuradas en '.env'.

[3] Puertos de Red:
  🟢 Puerto 4589   -> Puerto 4589 (Ecommerce REST API) está disponible.

[4] Dependencias del Proyecto:
  🟢 Gestor npm    -> Directorio 'node_modules' presente.

✨ ¡Excelente! El entorno cumple con todos los requisitos para comenzar a desarrollar.
```

---

### Caso B: Proyecto con Fallas Habituales (`app-with-issues`)
- **Entrada:** Falta el archivo `.env` (solo existe plantilla) y la carpeta `node_modules` no existe.
- **Resultado Esperado:** Código de salida `1`, semáforo `🔴 ACCIONES BLOQUEANTES (FAIL)` y lista de soluciones:
```text
Resultado: 🔴 BLOQUEANTE (FAIL)

[2] Variables de Entorno:
  🔴 Archivo .env       -> Falta el archivo '.env' en la raíz del proyecto.

[4] Dependencias del Proyecto:
  🔴 Gestor npm         -> Carpeta de dependencias 'node_modules' no existe.

🛠️  ACCIONES DE REMEDIACIÓN RECOMENDADAS:
  1. Crea '.env' ejecutando: cp .env.example .env
  2. Instala las dependencias del proyecto ejecutando: npm install
```

---

### Caso C: Manejo de Entradas Inválidas y Errores
La herramienta maneja con resiliencia los fallos comunes sin colapsar:

1. **Archivo JSON Corrupto (`app-corrupted`):**
   - **Comando:** `python3 doctor.py --project demo-projects/app-corrupted`
   - **Respuesta:**
     ```text
     ❌ Error de Configuración: Error de sintaxis JSON en '.../onboarding-profile.json':
     Línea 7, Columna 3: Expecting property name enclosed in double quotes
     ```
   - *Código de salida:* `2` (Error de configuración controlado).

2. **Ruta Inexistente:**
   - **Comando:** `python3 doctor.py --project /ruta/inventada_404`
   - **Respuesta:**
     ```text
     ❌ Error: La ruta especificada no existe: '/ruta/inventada_404'
     ```

---

## 💡 Decisiones de Diseño y Arquitectura

1. **Cero Dependencias de Terceros (`Zero Third-Party Deps`):**
   Se utilizó exclusivamente la biblioteca estándar (`json`, `socket`, `subprocess`, `re`, `shutil`, `argparse`, `pathlib`, `unittest`). Esto elimina cualquier riesgo de incompatibilidad de entornos durante la corrección o presentación.
2. **Detección de Puertos por Sockets TCP:**
   En lugar de depender de utilidades del sistema como `lsof` o `netstat` (cuyos comandos varían entre Linux, macOS y Windows), se emplea `socket.connect_ex`, logrando compatibilidad multiplataforma nativa.
3. **Desacoplamiento Mediante Contrato de Perfil:**
   El archivo `onboarding-profile.json` desacopla la lógica de comprobación de los proyectos concretos, permitiendo que la skill sea universalmente aplicable a proyectos Node.js, Python, PHP, Go o Docker.
