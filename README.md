# 🩺 Developer Onboarding Doctor

> **Skill inteligente para agentes de IA que diagnostica, valida y asiste en la configuración de entornos de desarrollo local en proyectos recién clonados.**

[![Skill Standard: Antigravity/Codex](https://img.shields.io/badge/Skill-Antigravity%20%2F%20Codex-blue)](https://github.com)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-green.svg)](https://python.org)
[![Status: Functional](https://img.shields.io/badge/Status-100%25%20Functional-brightgreen)](https://github.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)

---

## 📋 Índice
1. [¿Cuándo y Para Qué Utilizar esta Skill?](#-cuándo-y-para-qué-utilizar-esta-skill)
2. [Estructura del Proyecto y la Skill](#-estructura-del-proyecto-y-la-skill)
3. [Requisitos e Instalación de la Skill](#-requisitos-e-instalación-de-la-skill)
4. [Cómo Invocar la Skill con el Agente de IA](#-cómo-invocar-la-skill-con-el-agente-de-ia)
5. [Casos de Prueba y Demostración (Éxito vs Errores)](#-casos-de-prueba-y-demostración-éxito-vs-errores)
6. [Decisiones de Diseño y Arquitectura](#-decisiones-de-diseño-y-arquitectura)

---

## 🎯 ¿Cuándo y Para Qué Utilizar esta Skill?

### El Problema
Al clonar un repositorio o incorporarse a un nuevo equipo de desarrollo (*onboarding*), los desarrolladores pierden horas enfrentando problemas silenciosos de configuración:
- No se cuenta con la versión correcta de Node.js o Python en la máquina local.
- Faltan herramientas de consola obligatorias en el `$PATH` (como `git`, `npm` o `docker`).
- Los puertos de red requeridos (ej. `3000`, `5432`, `8080`) están ocupados por otros procesos o servicios activos.
- El archivo `.env` no existe o no tiene las variables de entorno mínimas requeridas respecto a `.env.example`.
- Las carpetas de dependencias (`node_modules`, `.venv`) no fueron instaladas.

### La Solución
**`developer-onboarding-doctor`** es una habilidad diseñada para el agente de IA que automatiza el proceso de diagnóstico de punta a punta:
1. Inspecciona los requisitos del proyecto a través de `onboarding-profile.json` (o los inicializa automáticamente).
2. Evalúa en milisegundos runtimes, versiones SemVer, puertos TCP, variables y dependencias.
3. Emite un semáforo visual inmediato (**🟢 PASS**, **🟡 WARN**, **🔴 FAIL**).
4. Genera comandos de remediación instantánea (`--fix-env`, liberación de puertos) y un informe Markdown enriquecido (`ONBOARDING_DIAGNOSIS.md`).

---

## 📂 Estructura del Proyecto y la Skill

El proyecto cumple estrictamente con el estándar oficial de skills para agentes de inteligencia artificial:

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
├── demo-projects/                                # Proyectos de prueba para la demostración con el agente
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
└── README.md                                     # Documentación integral del proyecto
```

### Justificación de Archivos y Carpetas:
- **`SKILL.md`**: El archivo principal que lee el agente inteligente. Contiene las directivas de activación (`description`) y el procedimiento paso a paso que el agente sigue de forma autónoma.
- **`scripts/doctor.py`**: Motor determinista en Python 3 puro (sin dependencias de `pip`) que el agente ejecuta mediante su herramienta de comandos para obtener el diagnóstico del sistema sin alucinar.
- **`assets/project_profile_schema.json`**: Esquema de validación para garantizar que los perfiles tengan un formato consistente.
- **`assets/default_profile.json`**: Plantilla utilizada por el agente para inicializar nuevos proyectos con `--init`.
- **`assets/report_template.md`**: Plantilla procesada dinámicamente para generar informes de onboarding en formato Markdown.
- **`references/troubleshooting_playbook.md`**: Manual técnico consultado por el agente para sugerir soluciones exactas al desarrollador.
- **`references/environment_standards.md`**: Fundamentos de ingeniería de software basados en *Twelve-Factor App*.

---

## ⚙️ Requisitos e Instalación de la Skill

### Requisitos Previos:
- **Python 3.10 o superior** (biblioteca estándar, sin necesidad de librerías externas).
- **Entorno de Agente de IA** (Google Antigravity, Codex o compatible).

### Instalación de la Skill en el Agente:
Para que el agente de IA reconozca la skill automáticamente en cualquier conversación:

```bash
# Copiar la skill a la carpeta global de skills del entorno
mkdir -p ~/.gemini/config/skills/developer-onboarding-doctor
cp -r .agents/skills/developer-onboarding-doctor/* ~/.gemini/config/skills/developer-onboarding-doctor/
```
*(También puede mantenerse directamente dentro de la carpeta `.agents/skills/` del repositorio).*

---

## 🤖 Cómo Invocar la Skill con el Agente de IA

La skill está diseñada para interactuar mediante **lenguaje natural** o invocación directa con **`@`** en el chat del agente:

### Invocación Directa (Etiquetando la Skill):
```text
@developer-onboarding-doctor revisa el proyecto demo-projects/app-success
```

### Invocación Natural (Activación Automática por Intención):
```text
"Acabo de clonar este repositorio y no arranca, ¿puedes verificar si el entorno cumple con todos los requisitos?"
```

### ¿Qué hace el Agente internamente al ser invocado?
1. Detecta la intención del usuario y lee las instrucciones de `SKILL.md`.
2. Ejecuta en segundo plano `scripts/doctor.py` apuntando a la ruta del proyecto.
3. Evalúa los resultados (runtimes, puertos libres, variables `.env`, dependencias).
4. Si detecta problemas, consulta `references/troubleshooting_playbook.md` y responde en el chat con el diagnóstico visual y las soluciones listas para aplicar.

---

## 🧪 Casos de Prueba y Demostración (Éxito vs Errores)

La validación y prueba de la skill se realiza interactuando con el agente a través de los proyectos de prueba incluidos:

---

### Caso 1: Proyecto Exitoso (`app-success`) — *Happy Path*
**Prompt de ejecución:**
> `@developer-onboarding-doctor haz un diagnóstico de demo-projects/app-success`

#### Resultado del Agente:
El agente reporta que todos los requisitos están cumplidos emitiendo el semáforo **🟢 TODO LISTO (PASS)**:
- 🟢 **Runtimes & CLI:** Versiones de Node.js y Python compatibles, herramientas `git` y `npm` disponibles.
- 🟢 **Variables de Entorno:** `.env` presente con todas las variables requeridas.
- 🟢 **Puertos:** Puerto libre y disponible.
- 🟢 **Dependencias:** `node_modules` instalado.
- Genera el reporte formal `ONBOARDING_DIAGNOSIS.md` en la raíz del proyecto.

---

### Caso 2: Detección de Problemas y Auto-Remediación (`app-with-issues`)
**Prompt de ejecución:**
> `@developer-onboarding-doctor diagnostica demo-projects/app-with-issues y dime qué falta`

#### Resultado del Agente:
El agente detecta las discrepancias críticas y emite el semáforo **🔴 BLOQUEANTE (FAIL)**:
- 🔴 **Variables de Entorno:** Falta el archivo `.env` en la raíz del proyecto.
- 🔴 **Dependencias:** Falta la carpeta `node_modules`.
- El agente sugiere inmediatamente la solución:
  ```bash
  # Copiar la plantilla de variables
  cp .env.example .env
  # Instalar dependencias
  npm install
  ```
*(Opcionalmente, se puede solicitar al agente aplicar la auto-reparación de variables con `--fix-env`).*

---

### Caso 3: Manejo de Entradas Inválidas y Archivos Corruptos (`app-corrupted`)
**Prompt de ejecución:**
> `@developer-onboarding-doctor revisa demo-projects/app-corrupted`

#### Resultado del Agente:
El agente identifica de inmediato el error de formato sin colapsar:
```text
❌ Error de Configuración: Error de sintaxis JSON en '.../onboarding-profile.json':
Línea 8, Columna 9: Expecting value
```
El agente explica que el archivo de configuración tiene una coma extra y orienta sobre cómo corregir la sintaxis.

---

### Caso 4: Ruta de Proyecto Inexistente (Error 404)
**Prompt de ejecución:**
> `@developer-onboarding-doctor revisa carpeta_inexistente`

#### Resultado del Agente:
El agente valida la ruta antes de proceder e informa con un mensaje de error controlado:
```text
❌ Error: La ruta especificada no existe: 'carpeta_inexistente'
```

---

## 💡 Decisiones de Diseño y Arquitectura

1. **Flujo Centrado en el Agente de IA:**
   A diferencia de scripts tradicionales que requieren memorizar comandos y flags en consola, la skill está desacoplada para que el agente sea quien orqueste el diagnóstico, interprete los códigos de salida y traduzca los resultados técnicos en recomendaciones comprensibles.
2. **Cero Dependencias de Terceros (`Zero Third-Party Deps`):**
   El motor `doctor.py` está escrito 100% en la biblioteca estándar de Python (`json`, `socket`, `subprocess`, `re`, `shutil`, `argparse`, `pathlib`, `unittest`). Esto garantiza que la skill funcione en cualquier máquina o contenedor sin necesidad de ejecutar `pip install`.
3. **Detección de Puertos por Sockets TCP:**
   En lugar de invocar utilidades del sistema operativo como `lsof` o `netstat` (cuyos argumentos y disponibilidad varían entre Linux, macOS y Windows), se emplea `socket.connect_ex` sobre `127.0.0.1`, logrando compatibilidad multiplataforma nativa.
4. **Desacoplamiento Mediante Contrato de Perfil:**
   El archivo `onboarding-profile.json` desacopla la lógica de comprobación de los proyectos concretos, permitiendo que la skill sea universalmente aplicable a proyectos Node.js, Python, Go o Docker.
