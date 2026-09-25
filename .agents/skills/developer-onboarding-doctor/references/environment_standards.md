# 📐 Estándares de Configuración de Entornos de Desarrollo

Este documento establece las mejores prácticas y principios de ingeniería para garantizar entornos de desarrollo reproducibles, seguros y consistentes entre todos los miembros de un equipo de software.

---

## 1. Principio Twelve-Factor App: Configuración

De acuerdo con el estándar de la industria [12-Factor App (Factor III: Config)](https://12factor.net/config):

- **La configuración que varía entre implementaciones (desarrollo, staging, producción) debe separarse estrictamente del código.**
- Nunca se deben almacenar credenciales, secretos ni URLs de bases de datos directamente en el código fuente.
- Todo repositorio debe proveer un archivo `.env.example` versionado en Git con valores dummy o explicativos.
- El archivo `.env` con secretos locales reales debe estar siempre presente en `.gitignore`.

---

## 2. Determinismo de Runtimes y Dependencias

Para evitar el clásico problema *"en mi máquina sí funciona"*:

1. **Lockfiles Obligatorios:**
   - Proyectos Node.js deben versionar `package-lock.json` o `pnpm-lock.yaml`.
   - Proyectos Python deben usar `requirements.lock` o `poetry.lock`.
2. **Especificación de Versiones de Motores (`engines`):**
   - En `package.json`, declarar el bloque:
     ```json
     "engines": {
       "node": ">=18.0.0",
       "npm": ">=9.0.0"
     }
     ```
3. **Control de Puertos:**
   - Evitar puertos arbitrarios no documentados. Declarar explícitamente en variables de entorno el puerto predeterminado con fallback (`process.env.PORT || 3000`).

---

## 3. Matriz de Severidad del Onboarding Doctor

| Severidad | Significado | Comportamiento del Desarrollador |
| :---: | :--- | :--- |
| 🟢 **PASS** | El requerimiento se cumple satisfactoriamente. | Ninguna acción necesaria. |
| 🟡 **WARN** | Requerimiento secundario o no crítico ausente. | El proyecto puede iniciar, pero ciertas funciones fallarán. |
| 🔴 **FAIL** | Requerimiento crítico faltante (versión de runtime incompatible, dependencias no instaladas, puerto tomado). | **Bloqueante.** Debe resolverse antes de ejecutar `npm run dev` o `python main.py`. |
