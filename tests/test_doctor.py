#!/usr/bin/env python3
"""
Suite de Pruebas Unitarias Automatizadas para 'developer-onboarding-doctor'.
Verifica casos de éxito, advertencias, manejo de errores y generación de reportes.
"""

import sys
import unittest
import tempfile
import shutil
from pathlib import Path

# Agregar la ruta del script al sys.path
TEST_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TEST_DIR.parent
SKILL_SCRIPTS = PROJECT_ROOT / ".agents" / "skills" / "developer-onboarding-doctor" / "scripts"
sys.path.insert(0, str(SKILL_SCRIPTS))

from doctor import OnboardingDoctor, parse_semver, is_port_in_use


class TestOnboardingDoctor(unittest.TestCase):
    def setUp(self):
        self.demo_dir = PROJECT_ROOT / "demo-projects"
        self.app_success = self.demo_dir / "app-success"
        self.app_issues = self.demo_dir / "app-with-issues"
        self.app_corrupted = self.demo_dir / "app-corrupted"

    def test_parse_semver(self):
        """Verifica la correcta descomposición de versiones semánticas."""
        self.assertEqual(parse_semver("18.12.0"), (18, 12, 0))
        self.assertEqual(parse_semver("v20.10.0"), (20, 10, 0))
        self.assertEqual(parse_semver("3.11"), (3, 11, 0))
        self.assertEqual(parse_semver("invalid"), (0, 0, 0))
        self.assertTrue(parse_semver("20.0.0") > parse_semver("18.5.2"))

    def test_invalid_project_path(self):
        """Prueba de manejo de errores ante una ruta inexistente."""
        fake_path = PROJECT_ROOT / "non_existent_folder_xyz_123"
        doc = OnboardingDoctor(fake_path)
        valid, msg = doc.validate_project_path()
        self.assertFalse(valid)
        self.assertIn("no existe", msg)

    def test_corrupted_json_handled_gracefully(self):
        """Prueba de manejo de error ante un JSON malformado."""
        doc = OnboardingDoctor(self.app_corrupted)
        valid_path, _ = doc.validate_project_path()
        self.assertTrue(valid_path)

        loaded, err = doc.load_profile()
        self.assertFalse(loaded)
        self.assertIn("Error de sintaxis JSON", err)

    def test_successful_project_validation(self):
        """Prueba del caso de éxito: proyecto app-success."""
        doc = OnboardingDoctor(self.app_success)
        loaded, err = doc.load_profile()
        self.assertTrue(loaded, f"Error cargando perfil: {err}")

        doc.run_all_checks()
        # En un entorno de desarrollo estándar, app-success no debe tener fallos bloqueantes
        self.assertEqual(doc.summary["fail"], 0, f"Fallos inesperados: {doc.results}")
        self.assertIn(doc.get_overall_status(), ["PASS", "WARN"])

    def test_issues_project_detection(self):
        """Prueba detección de problemas: falta de .env y dependencias."""
        doc = OnboardingDoctor(self.app_issues)
        loaded, _ = doc.load_profile()
        self.assertTrue(loaded)

        doc.run_all_checks()
        # Debe haber detectado al menos la falta del .env y dependencias
        self.assertGreater(doc.summary["fail"], 0)
        self.assertEqual(doc.get_overall_status(), "FAIL")

        # Verificar que el mensaje de remediación para .env esté presente
        remediation_text = " ".join(doc.remediations)
        self.assertTrue(".env" in remediation_text or "npm" in remediation_text)

    def test_fix_env_feature(self):
        """Prueba la funcionalidad de autocorrección de .env."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            # Crear .env.example
            example_file = temp_path / ".env.example"
            example_file.write_text("PORT=8000\nSECRET=test", encoding="utf-8")

            # Crear profile
            profile_file = temp_path / "onboarding-profile.json"
            profile_file.write_text("""{
                "projectName": "temp-test",
                "runtimes": [],
                "env": {
                    "envFile": ".env",
                    "exampleFile": ".env.example"
                }
            }""", encoding="utf-8")

            doc = OnboardingDoctor(temp_path)
            doc.load_profile()

            # Verificar que .env no existe antes
            env_file = temp_path / ".env"
            self.assertFalse(env_file.exists())

            # Aplicar corrección
            ok, msg = doc.fix_env()
            self.assertTrue(ok)
            self.assertTrue(env_file.exists())
            self.assertEqual(env_file.read_text(encoding="utf-8"), example_file.read_text(encoding="utf-8"))

    def test_markdown_report_generation(self):
        """Verifica la generación del reporte Markdown a partir de la plantilla."""
        doc = OnboardingDoctor(self.app_success)
        doc.load_profile()
        doc.run_all_checks()

        with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as tmp:
            tmp_report = Path(tmp.name)

        try:
            ok, msg = doc.generate_markdown_report(tmp_report)
            self.assertTrue(ok, f"Fallo al generar reporte: {msg}")
            self.assertTrue(tmp_report.exists())
            content = tmp_report.read_text(encoding="utf-8")
            self.assertIn("ecommerce-api-success", content)
            self.assertIn("Resumen Ejecutivo", content)
        finally:
            if tmp_report.exists():
                tmp_report.unlink()


if __name__ == "__main__":
    unittest.main(verbosity=2)
