# 📘 Troubleshooting Playbook: Resolución de Problemas de Entorno

Este manual proporciona instrucciones paso a paso para resolver las discrepancias y fallos detectados por `developer-onboarding-doctor`.

---

## 1. Puertos de Red Ocupados (Network Port Collisions)

### Síntoma
El diagnóstico arroja: `🔴 FAIL: Puerto 3000 ocupado por otro proceso`.

### Causa Raíz
Otra aplicación (o una instancia previa de tu servidor en segundo plano) ya está escuchando en ese puerto TCP.

### Solución en Linux / macOS:
1. **Identificar qué proceso tiene tomado el puerto:**
   ```bash
   lsof -i :3000
   # o bien:
   ss -lptn 'sport = :3000'
   ```
2. **Terminar el proceso:**
   ```bash
   kill -9 <PID>
   # O directamente por puerto:
   fuser -k 3000/tcp
   ```

### Solución en Windows (PowerShell):
1. **Identificar y matar:**
   ```powershell
   Get-Process -Id (Get-NetTCPConnection -LocalPort 3000).OwningProcess | Stop-Process -Force
   ```

---

## 2. Variables de Entorno Faltantes (.env)

### Síntoma
`🔴 FAIL: El archivo .env no existe en la raíz del proyecto` o `🟡 WARN: Faltan las variables [DATABASE_URL, API_SECRET_KEY]`.

### Causa Raíz
Los proyectos seguros nunca commitean `.env` al repositorio de git. Quien clona el proyecto debe inicializar su archivo local copiando la plantilla.

### Solución:
1. **Copiar la plantilla de ejemplo:**
   ```bash
   cp .env.example .env
   ```
   *(También puedes usar el comando automático de la skill: `python3 doctor.py --fix-env`)*.
2. **Configurar los valores reales requeridos** en `.env` (credenciales locales de base de datos, llaves API de prueba).

---

## 3. Versiones Incompatibles de Node.js o Python

### Síntoma
`🔴 FAIL: node versión 16.14.0 instalada, se requiere >= 18.0.0`.

### Causa Raíz
Tu máquina local tiene una versión antigua del motor de ejecución que carece de soporte para APIs modernas (como `fetch` global en Node 18+ o type hinting moderno en Python 3.10+).

### Solución para Node.js (usando NVM):
```bash
# Instalar la versión recomendada
nvm install 20
nvm use 20
node -v
```

### Solución para Python (usando pyenv o paquetes de sistema):
```bash
# Con pyenv:
pyenv install 3.11.8
pyenv local 3.11.8

# En Ubuntu/Debian:
sudo apt update && sudo apt install python3.11 python3.11-venv
```

---

## 4. Dependencias del Proyecto No Instaladas

### Síntoma
`🔴 FAIL: Directorio node_modules no encontrado` o `🔴 FAIL: Entorno virtual .venv no encontrado`.

### Causa Raíz
El repositorio recién clonado no tiene instalados los módulos de dependencias locales.

### Solución para proyectos Node.js:
```bash
# Si existe package-lock.json (instalación limpia y determinista):
npm ci
# O instalación estándar:
npm install
```

### Solución para proyectos Python:
```bash
# Crear entorno virtual si no existe:
python3 -m venv .venv
source .venv/bin/activate

# Instalar requerimientos:
pip install -r requirements.txt
```

---

## 5. Herramientas CLI Faltantes en el PATH

### Síntoma
`🔴 FAIL: Herramienta 'docker' no encontrada en PATH`.

### Solución:
Verifica si el binario está instalado en una ruta no listada en tu variable `$PATH` o instálalo con tu gestor de paquetes preferido (`apt`, `brew`, `choco`).
