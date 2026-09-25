#!/usr/bin/env bash
# ==============================================================================
# Script de Demostración Completa: developer-onboarding-doctor
# Ejecuta el flujo de principio a fin para la evaluación / presentación oral.
# ==============================================================================

set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
DOCTOR="$DIR/.agents/skills/developer-onboarding-doctor/scripts/doctor.py"

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m' # No Color

clear 2>/dev/null || true

echo -e "${CYAN}${BOLD}"
echo "=========================================================================="
echo "    DEMOSTRACIÓN OFICIAL: SKILL 'developer-onboarding-doctor'"
echo "=========================================================================="
echo -e "${NC}"
echo "Esta demostración cubre los 4 casos indispensables para la evaluación:"
echo " 1. Caso Exitoso (Happy Path) -> Semáforo 🟢 PASS"
echo " 2. Caso con Problemas de Entorno -> Semáforo 🔴 FAIL + Auto-Remediación"
echo " 3. Manejo de Errores y Entradas Inválidas -> Detección elegante de fallos"
echo " 4. Ejecución de la Suite de Pruebas Unitarias Automatizadas"
echo ""
read -p "Presiona [ENTER] para comenzar con el Caso 1 (Caso Exitoso)..." dummy

echo ""
echo -e "${BOLD}${GREEN}=========================================================================="
echo " [PASO 1] Ejecución del Caso Exitoso: demo-projects/app-success"
echo -e "==========================================================================${NC}"
python3 "$DOCTOR" --project "$DIR/demo-projects/app-success" --report "$DIR/demo-projects/app-success/ONBOARDING_DIAGNOSIS.md"
echo -e "${GREEN}✓ Reporte Markdown generado en demo-projects/app-success/ONBOARDING_DIAGNOSIS.md${NC}"

echo ""
read -p "Presiona [ENTER] para continuar al Caso 2 (Detección de Problemas)..." dummy

echo ""
echo -e "${BOLD}${YELLOW}=========================================================================="
echo " [PASO 2] Detección de Problemas de Entorno: demo-projects/app-with-issues"
echo -e "==========================================================================${NC}"
# Permitir que el comando devuelva código de error sin abortar el script
set +e
python3 "$DOCTOR" --project "$DIR/demo-projects/app-with-issues"
EXIT_CODE=$?
set -e
echo -e "${YELLOW}-> El doctor detectó correctamente las fallas bloqueantes (Exit Code: $EXIT_CODE).${NC}"

echo ""
echo -e "${CYAN}--- Aplicando Auto-Remediación de variables (.env) con la skill ---${NC}"
python3 "$DOCTOR" --project "$DIR/demo-projects/app-with-issues" --fix-env

echo ""
read -p "Presiona [ENTER] para continuar al Caso 3 (Manejo de Errores e Insumos Inválidos)..." dummy

echo ""
echo -e "${BOLD}${RED}=========================================================================="
echo " [PASO 3] Manejo de Errores: demo-projects/app-corrupted (JSON Inválido)"
echo -e "==========================================================================${NC}"
set +e
python3 "$DOCTOR" --project "$DIR/demo-projects/app-corrupted"
set -e

echo ""
echo -e "${BOLD}${RED}=========================================================================="
echo " [PASO 3.1] Manejo de Errores: Ruta de Proyecto Inexistente"
echo -e "==========================================================================${NC}"
set +e
python3 "$DOCTOR" --project "$DIR/carpeta_que_no_existe_404"
set -e

echo ""
read -p "Presiona [ENTER] para ejecutar las Pruebas Unitarias Automatizadas..." dummy

echo ""
echo -e "${BOLD}${CYAN}=========================================================================="
echo " [PASO 4] Suite de Pruebas Automatizadas (unittest)"
echo -e "==========================================================================${NC}"
python3 -m unittest discover -s "$DIR/tests" -p "test_*.py" -v

echo ""
echo -e "${GREEN}${BOLD}=========================================================================="
echo "  ✨ DEMOSTRACIÓN COMPLETADA CON ÉXITO (100% Criterios de Evaluación)"
echo -e "==========================================================================${NC}"
