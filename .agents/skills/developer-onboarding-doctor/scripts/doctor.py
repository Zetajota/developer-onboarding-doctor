#!/usr/bin/env python3
"""
developer-onboarding-doctor
Script de diagnóstico y validación de entornos de desarrollo local.
Diseñado para la skill 'developer-onboarding-doctor'.
"""

import sys
import os
import re
import json
import shutil
import socket
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

# Rutas relativas a la estructura de la skill
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
ASSETS_DIR = SKILL_ROOT / "assets"
REFERENCES_DIR = SKILL_ROOT / "references"


class Colors:
    """Códigos ANSI para salida con colores en terminal."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RED = "\033[31m"
    BLUE = "\033[34m"
    CYAN = "\033[36m"
    GRAY = "\033[90m"

    @classmethod
    def disable_if_no_tty(cls):
        if not sys.stdout.isatty():
            cls.RESET = ""
            cls.BOLD = ""
            cls.GREEN = ""
            cls.YELLOW = ""
            cls.RED = ""
            cls.BLUE = ""
            cls.CYAN = ""
            cls.GRAY = ""


def parse_semver(version_str: str):
    """Extrae tupla (major, minor, patch) de una cadena de versión."""
    match = re.search(r"(\d+)(?:\.(\d+))?(?:\.(\d+))?", version_str)
    if not match:
        return (0, 0, 0)
    major = int(match.group(1) or 0)
    minor = int(match.group(2) or 0)
    patch = int(match.group(3) or 0)
    return (major, minor, patch)


def is_port_in_use(port: int, host: str = "127.0.0.1") -> bool:
    """Verifica si un puerto TCP local está ocupado."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.4)
        result = sock.connect_ex((host, port))
        return result == 0


class OnboardingDoctor:
    def __init__(self, project_dir: Path):
        self.project_dir = project_dir.resolve()
        self.profile = {}
        self.results = {
            "runtimes": [],
            "clis": [],
            "env": [],
            "ports": [],
            "dependencies": []
        }
        self.summary = {"pass": 0, "warn": 0, "fail": 0}
        self.remediations = []

    def validate_project_path(self):
        """Verifica que la ruta del proyecto exista y sea un directorio."""
        if not self.project_dir.exists():
            return False, f"La ruta especificada no existe: '{self.project_dir}'"
        if not self.project_dir.is_dir():
            return False, f"La ruta no es un directorio válido: '{self.project_dir}'"
        return True, ""

    def load_profile(self):
        """Carga y valida el archivo onboarding-profile.json."""
        profile_path = self.project_dir / "onboarding-profile.json"
        if not profile_path.exists():
            return False, (
                f"No se encontró 'onboarding-profile.json' en {self.project_dir}.\n"
                f"Sugerencia: Ejecuta 'doctor.py --project {self.project_dir} --init' "
                f"para crear una plantilla base."
            )

        try:
            with open(profile_path, "r", encoding="utf-8") as f:
                self.profile = json.load(f)
        except json.JSONDecodeError as err:
            return False, (
                f"Error de sintaxis JSON en '{profile_path}':\n"
                f"Línea {err.lineno}, Columna {err.colno}: {err.msg}"
            )
        except Exception as err:
            return False, f"No se pudo leer el archivo de perfil: {err}"

        # Validaciones mínimas de estructura
        if not isinstance(self.profile, dict):
            return False, "El archivo de perfil debe ser un objeto JSON válido."

        if "projectName" not in self.profile:
            return False, "El perfil carece del campo obligatorio 'projectName'."

        if "runtimes" not in self.profile or not isinstance(self.profile.get("runtimes"), list):
            return False, "El perfil debe contener una lista 'runtimes'."

        return True, ""

    def init_profile(self):
        """Copia el perfil predeterminado de assets al proyecto."""
        profile_path = self.project_dir / "onboarding-profile.json"
        if profile_path.exists():
            return False, f"El archivo '{profile_path}' ya existe."

        default_asset = ASSETS_DIR / "default_profile.json"
        if not default_asset.exists():
            return False, f"Plantilla de asset no encontrada en: {default_asset}"

        try:
            with open(default_asset, "r", encoding="utf-8") as src:
                data = json.load(src)
            data["projectName"] = self.project_dir.name
            with open(profile_path, "w", encoding="utf-8") as dst:
                json.dump(data, dst, indent=2, ensure_ascii=False)
            return True, f"Perfil inicializado con éxito en: {profile_path}"
        except Exception as err:
            return False, f"Error al inicializar el perfil: {err}"

    def fix_env(self):
        """Copia .env.example a .env si este último no existe."""
        env_cfg = self.profile.get("env", {})
        env_file = self.project_dir / env_cfg.get("envFile", ".env")
        example_file = self.project_dir / env_cfg.get("exampleFile", ".env.example")

        if env_file.exists():
            return True, f"El archivo '{env_file.name}' ya existe."

        if not example_file.exists():
            return False, f"No existe la plantilla '{example_file.name}' para duplicar."

        try:
            shutil.copyfile(example_file, env_file)
            return True, f"Archivo '{env_file.name}' creado a partir de '{example_file.name}'."
        except Exception as err:
            return False, f"Error al duplicar .env: {err}"

    def check_runtimes(self):
        """Verifica la existencia y versiones mínimas de los runtimes declarados."""
        runtimes = self.profile.get("runtimes", [])
        for r in runtimes:
            name = r.get("name")
            min_ver = r.get("minVersion", "0.0.0")
            rec_ver = r.get("recommendedVersion", min_ver)

            bin_path = shutil.which(name)
            if not bin_path:
                self.results["runtimes"].append({
                    "name": name,
                    "status": "FAIL",
                    "message": f"Ejecutable '{name}' no encontrado en el PATH del sistema.",
                    "minVersion": min_ver,
                    "installedVersion": None
                })
                self.summary["fail"] += 1
                self.remediations.append(f"Instala '{name}' versión >= {min_ver} en tu sistema operativo.")
                continue

            # Obtener versión instalada
            installed_ver_str = self._get_version(name)
            if not installed_ver_str:
                self.results["runtimes"].append({
                    "name": name,
                    "status": "WARN",
                    "message": f"Instalado en '{bin_path}' pero no fue posible determinar la versión.",
                    "minVersion": min_ver,
                    "installedVersion": "Desconocida"
                })
                self.summary["warn"] += 1
                continue

            inst_parsed = parse_semver(installed_ver_str)
            min_parsed = parse_semver(min_ver)

            if inst_parsed >= min_parsed:
                self.results["runtimes"].append({
                    "name": name,
                    "status": "PASS",
                    "message": f"Versión {installed_ver_str} instalada (Requerida >= {min_ver}).",
                    "minVersion": min_ver,
                    "installedVersion": installed_ver_str
                })
                self.summary["pass"] += 1
            else:
                self.results["runtimes"].append({
                    "name": name,
                    "status": "FAIL",
                    "message": f"Versión {installed_ver_str} es menor a la requerida ({min_ver}).",
                    "minVersion": min_ver,
                    "installedVersion": installed_ver_str
                })
                self.summary["fail"] += 1
                self.remediations.append(f"Actualiza '{name}' de {installed_ver_str} a >= {min_ver} (Recomendada: {rec_ver}).")

    def _get_version(self, binary: str) -> str:
        """Intenta extraer la versión de un comando de sistema."""
        commands = [
            [binary, "--version"],
            [binary, "-v"],
            [binary, "-V"]
        ]
        for cmd in commands:
            try:
                proc = subprocess.run(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=2
                )
                output = proc.stdout.strip() or proc.stderr.strip()
                if output:
                    match = re.search(r"(\d+\.\d+(?:\.\d+)?)", output)
                    if match:
                        return match.group(1)
            except Exception:
                continue
        return ""

    def check_clis(self):
        """Verifica que las utilidades de consola requeridas estén en PATH."""
        clis = self.profile.get("requiredCLIs", [])
        for cli in clis:
            bin_path = shutil.which(cli)
            if bin_path:
                self.results["clis"].append({
                    "name": cli,
                    "status": "PASS",
                    "message": f"Disponible en: {bin_path}"
                })
                self.summary["pass"] += 1
            else:
                self.results["clis"].append({
                    "name": cli,
                    "status": "FAIL",
                    "message": f"Comando '{cli}' ausente en PATH."
                })
                self.summary["fail"] += 1
                self.remediations.append(f"Instala la herramienta CLI '{cli}' en tu PATH.")

    def check_env(self):
        """Verifica la existencia del archivo .env y sus variables requeridas."""
        env_cfg = self.profile.get("env")
        if not env_cfg:
            return

        env_file_name = env_cfg.get("envFile", ".env")
        example_file_name = env_cfg.get("exampleFile", ".env.example")
        required_keys = env_cfg.get("requiredKeys", [])

        env_path = self.project_dir / env_file_name
        example_path = self.project_dir / example_file_name

        if not env_path.exists():
            self.results["env"].append({
                "check": "Archivo .env",
                "status": "FAIL",
                "message": f"Falta el archivo '{env_file_name}' en la raíz del proyecto."
            })
            self.summary["fail"] += 1
            if example_path.exists():
                self.remediations.append(f"Crea '{env_file_name}' ejecutando: cp {example_file_name} {env_file_name}")
            else:
                self.remediations.append(f"Crea el archivo '{env_file_name}' con las variables necesarias.")
            return

        # Leer variables existentes en .env
        existing_keys = set()
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, _ = line.split("=", 1)
                        existing_keys.add(k.strip())
        except Exception as err:
            self.results["env"].append({
                "check": "Lectura .env",
                "status": "WARN",
                "message": f"No se pudo parsear '{env_file_name}': {err}"
            })
            self.summary["warn"] += 1
            return

        missing_keys = [k for k in required_keys if k not in existing_keys]
        if missing_keys:
            self.results["env"].append({
                "check": "Variables requeridas",
                "status": "WARN",
                "message": f"Faltan definir las siguientes variables en '{env_file_name}': {', '.join(missing_keys)}"
            })
            self.summary["warn"] += 1
            self.remediations.append(f"Agrega los valores para [{', '.join(missing_keys)}] en tu '{env_file_name}'.")
        else:
            self.results["env"].append({
                "check": "Variables requeridas",
                "status": "PASS",
                "message": f"Todas las variables clave ({len(required_keys)}) están configuradas en '{env_file_name}'."
            })
            self.summary["pass"] += 1

    def check_ports(self):
        """Verifica si los puertos configurados para la app están libres."""
        ports = self.profile.get("ports", [])
        for p in ports:
            port_num = p.get("port")
            service = p.get("service", "Servicio")
            is_critical = p.get("critical", True)

            in_use = is_port_in_use(port_num)
            if in_use:
                status = "FAIL" if is_critical else "WARN"
                if status == "FAIL":
                    self.summary["fail"] += 1
                else:
                    self.summary["warn"] += 1

                self.results["ports"].append({
                    "port": port_num,
                    "service": service,
                    "status": status,
                    "message": f"Puerto {port_num} ({service}) está OCUPADO por otro proceso."
                })
                self.remediations.append(
                    f"Libera el puerto {port_num} o finaliza el proceso con: lsof -i :{port_num} y kill -9 <PID>"
                )
            else:
                self.results["ports"].append({
                    "port": port_num,
                    "service": service,
                    "status": "PASS",
                    "message": f"Puerto {port_num} ({service}) está disponible."
                })
                self.summary["pass"] += 1

    def check_dependencies(self):
        """Verifica la presencia de la carpeta de dependencias del proyecto."""
        dep_cfg = self.profile.get("dependencies")
        if not dep_cfg:
            return

        dep_type = dep_cfg.get("type", "npm")
        install_dir_name = dep_cfg.get("installDir", "node_modules")
        lock_file_name = dep_cfg.get("lockFile", "package-lock.json")

        install_dir = self.project_dir / install_dir_name
        lock_file = self.project_dir / lock_file_name

        if not install_dir.exists():
            self.results["dependencies"].append({
                "type": dep_type,
                "status": "FAIL",
                "message": f"Carpeta de dependencias '{install_dir_name}' no existe."
            })
            self.summary["fail"] += 1
            if dep_type == "npm":
                cmd = "npm ci" if lock_file.exists() else "npm install"
                self.remediations.append(f"Instala las dependencias del proyecto ejecutando: {cmd}")
            elif dep_type == "pip":
                self.remediations.append("Instala las dependencias ejecutando: pip install -r requirements.txt")
            else:
                self.remediations.append(f"Instala las dependencias para {dep_type}.")
        else:
            self.results["dependencies"].append({
                "type": dep_type,
                "status": "PASS",
                "message": f"Directorio '{install_dir_name}' presente."
            })
            self.summary["pass"] += 1

    def run_all_checks(self):
        """Ejecuta toda la batería de comprobaciones."""
        self.check_runtimes()
        self.check_clis()
        self.check_env()
        self.check_ports()
        self.check_dependencies()

    def get_overall_status(self):
        """Determina el estado global (PASS, WARN o FAIL)."""
        if self.summary["fail"] > 0:
            return "FAIL"
        if self.summary["warn"] > 0:
            return "WARN"
        return "PASS"

    def print_terminal_report(self):
        """Imprime un reporte estilizado en consola."""
        project_name = self.profile.get("projectName", self.project_dir.name)
        overall = self.get_overall_status()

        badge = {
            "PASS": f"{Colors.GREEN}{Colors.BOLD}🟢 TODO LISTO (PASS){Colors.RESET}",
            "WARN": f"{Colors.YELLOW}{Colors.BOLD}🟡 ADVERTENCIAS (WARN){Colors.RESET}",
            "FAIL": f"{Colors.RED}{Colors.BOLD}🔴 BLOQUEANTE (FAIL){Colors.RESET}"
        }[overall]

        print(f"\n{Colors.CYAN}{Colors.BOLD}================================================================{Colors.RESET}")
        print(f"{Colors.BOLD}🩺 DEVELOPER ONBOARDING DOCTOR{Colors.RESET}")
        print(f"Proyecto : {Colors.BOLD}{project_name}{Colors.RESET}")
        print(f"Ubicación: {self.project_dir}")
        print(f"Resultado: {badge}")
        print(f"{Colors.CYAN}================================================================{Colors.RESET}\n")

        # Runtimes y CLIs
        print(f"{Colors.BOLD}[1] Runtimes y Herramientas del Sistema:{Colors.RESET}")
        for item in self.results["runtimes"]:
            icon = "🟢" if item["status"] == "PASS" else ("🟡" if item["status"] == "WARN" else "🔴")
            print(f"  {icon} {item['name']:<10} -> {item['message']}")
        for item in self.results["clis"]:
            icon = "🟢" if item["status"] == "PASS" else "🔴"
            print(f"  {icon} CLI:{item['name']:<6} -> {item['message']}")

        # Variables de entorno
        print(f"\n{Colors.BOLD}[2] Variables de Entorno:{Colors.RESET}")
        for item in self.results["env"]:
            icon = "🟢" if item["status"] == "PASS" else ("🟡" if item["status"] == "WARN" else "🔴")
            print(f"  {icon} {item['check']:<18} -> {item['message']}")

        # Puertos de red
        print(f"\n{Colors.BOLD}[3] Puertos de Red:{Colors.RESET}")
        for item in self.results["ports"]:
            icon = "🟢" if item["status"] == "PASS" else ("🟡" if item["status"] == "WARN" else "🔴")
            print(f"  {icon} Puerto {item['port']:<6} -> {item['message']}")

        # Dependencias
        print(f"\n{Colors.BOLD}[4] Dependencias del Proyecto:{Colors.RESET}")
        for item in self.results["dependencies"]:
            icon = "🟢" if item["status"] == "PASS" else "🔴"
            print(f"  {icon} Gestor {item['type']:<6} -> {item['message']}")

        # Plan de remediación
        if self.remediations:
            print(f"\n{Colors.YELLOW}{Colors.BOLD}🛠️  ACCIONES DE REMEDIACIÓN RECOMENDADAS:{Colors.RESET}")
            for idx, action in enumerate(self.remediations, 1):
                print(f"  {Colors.BOLD}{idx}.{Colors.RESET} {action}")
        else:
            print(f"\n{Colors.GREEN}{Colors.BOLD}✨ ¡Excelente! El entorno cumple con todos los requisitos para comenzar a desarrollar.{Colors.RESET}")

        print(f"\n{Colors.GRAY}Resumen: {self.summary['pass']} Pasados | {self.summary['warn']} Advertencias | {self.summary['fail']} Fallos{Colors.RESET}\n")

    def generate_markdown_report(self, output_path: Path):
        """Genera un archivo Markdown usando la plantilla en assets."""
        template_file = ASSETS_DIR / "report_template.md"
        if not template_file.exists():
            return False, f"Plantilla de reporte no encontrada en {template_file}"

        try:
            with open(template_file, "r", encoding="utf-8") as f:
                template = f.read()
        except Exception as err:
            return False, f"Error leyendo plantilla de reporte: {err}"

        overall = self.get_overall_status()
        badge_md = {
            "PASS": "🟢 **TODO LISTO (PASS)**",
            "WARN": "🟡 **ADVERTENCIAS (WARN)**",
            "FAIL": "🔴 **ACCIONES BLOQUEANTES (FAIL)**"
        }[overall]

        # Formatear detalles
        def format_section(items, key_field="message"):
            if not items:
                return "_No se configuraron comprobaciones para esta categoría._\n"
            lines = []
            for it in items:
                icon = "🟢" if it["status"] == "PASS" else ("🟡" if it["status"] == "WARN" else "🔴")
                lines.append(f"- {icon} **{it.get('name') or it.get('check') or it.get('port') or it.get('type')}:** {it[key_field]}")
            return "\n".join(lines) + "\n"

        remediation_md = ""
        if self.remediations:
            remediation_md = "Ejecuta los siguientes comandos o ajustes para completar el setup:\n\n"
            for i, r in enumerate(self.remediations, 1):
                remediation_md += f"{i}. {r}\n"
        else:
            remediation_md = "✨ **El entorno está 100% listo para programar y compilar.**\n"

        # Conteos por categoria
        rt_pass = sum(1 for x in self.results["runtimes"] + self.results["clis"] if x["status"] == "PASS")
        rt_warn = sum(1 for x in self.results["runtimes"] + self.results["clis"] if x["status"] == "WARN")
        rt_fail = sum(1 for x in self.results["runtimes"] + self.results["clis"] if x["status"] == "FAIL")
        rt_status = "🟢 PASS" if rt_fail == 0 and rt_warn == 0 else ("🟡 WARN" if rt_fail == 0 else "🔴 FAIL")

        env_pass = sum(1 for x in self.results["env"] if x["status"] == "PASS")
        env_warn = sum(1 for x in self.results["env"] if x["status"] == "WARN")
        env_fail = sum(1 for x in self.results["env"] if x["status"] == "FAIL")
        env_status = "🟢 PASS" if env_fail == 0 and env_warn == 0 else ("🟡 WARN" if env_fail == 0 else "🔴 FAIL")

        ports_pass = sum(1 for x in self.results["ports"] if x["status"] == "PASS")
        ports_warn = sum(1 for x in self.results["ports"] if x["status"] == "WARN")
        ports_fail = sum(1 for x in self.results["ports"] if x["status"] == "FAIL")
        ports_status = "🟢 PASS" if ports_fail == 0 and ports_warn == 0 else ("🟡 WARN" if ports_fail == 0 else "🔴 FAIL")

        dep_pass = sum(1 for x in self.results["dependencies"] if x["status"] == "PASS")
        dep_warn = sum(1 for x in self.results["dependencies"] if x["status"] == "WARN")
        dep_fail = sum(1 for x in self.results["dependencies"] if x["status"] == "FAIL")
        dep_status = "🟢 PASS" if dep_fail == 0 and dep_warn == 0 else ("🟡 WARN" if dep_fail == 0 else "🔴 FAIL")

        replacements = {
            "{{PROJECT_NAME}}": self.profile.get("projectName", self.project_dir.name),
            "{{TIMESTAMP}}": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "{{PROJECT_PATH}}": str(self.project_dir),
            "{{OVERALL_STATUS_BADGE}}": badge_md,
            "{{RUNTIMES_STATUS}}": rt_status,
            "{{RUNTIMES_PASS}}": str(rt_pass),
            "{{RUNTIMES_WARN}}": str(rt_warn),
            "{{RUNTIMES_FAIL}}": str(rt_fail),
            "{{ENV_STATUS}}": env_status,
            "{{ENV_PASS}}": str(env_pass),
            "{{ENV_WARN}}": str(env_warn),
            "{{ENV_FAIL}}": str(env_fail),
            "{{PORTS_STATUS}}": ports_status,
            "{{PORTS_PASS}}": str(ports_pass),
            "{{PORTS_WARN}}": str(ports_warn),
            "{{PORTS_FAIL}}": str(ports_fail),
            "{{DEPS_STATUS}}": dep_status,
            "{{DEPS_PASS}}": str(dep_pass),
            "{{DEPS_WARN}}": str(dep_warn),
            "{{DEPS_FAIL}}": str(dep_fail),
            "{{RUNTIMES_DETAILS}}": format_section(self.results["runtimes"] + self.results["clis"]),
            "{{ENV_DETAILS}}": format_section(self.results["env"]),
            "{{PORTS_DETAILS}}": format_section(self.results["ports"]),
            "{{DEPS_DETAILS}}": format_section(self.results["dependencies"]),
            "{{REMEDIATION_COMMANDS}}": remediation_md
        }

        content = template
        for k, v in replacements.items():
            content = content.replace(k, v)

        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(content)
            return True, f"Reporte Markdown guardado exitosamente en: {output_path}"
        except Exception as err:
            return False, f"Error escribiendo reporte: {err}"


def main():
    Colors.disable_if_no_tty()
    parser = argparse.ArgumentParser(
        description="developer-onboarding-doctor: Diagnóstico y validación de entornos de desarrollo local."
    )
    parser.add_argument(
        "--project", "-p",
        type=str,
        default=".",
        help="Ruta al proyecto a diagnosticar (por defecto: directorio actual)"
    )
    parser.add_argument(
        "--init",
        action="store_true",
        help="Inicializa un archivo 'onboarding-profile.json' base en el proyecto"
    )
    parser.add_argument(
        "--fix-env",
        action="store_true",
        help="Copia .env.example a .env automáticamente si este último falta"
    )
    parser.add_argument(
        "--report", "-r",
        type=str,
        help="Genera un reporte Markdown en la ruta especificada"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emite el diagnóstico en formato JSON estructurado"
    )

    args = parser.parse_args()
    project_path = Path(args.project)

    doctor = OnboardingDoctor(project_path)

    # 1. Validar ruta
    valid, err_msg = doctor.validate_project_path()
    if not valid:
        print(f"{Colors.RED}❌ Error:{Colors.RESET} {err_msg}", file=sys.stderr)
        sys.exit(2)

    # 2. Inicialización rápida
    if args.init:
        ok, msg = doctor.init_profile()
        color = Colors.GREEN if ok else Colors.RED
        print(f"{color}{msg}{Colors.RESET}")
        sys.exit(0 if ok else 2)

    # 3. Cargar perfil
    loaded, err_msg = doctor.load_profile()
    if not loaded:
        print(f"{Colors.RED}❌ Error de Configuración:{Colors.RESET} {err_msg}", file=sys.stderr)
        sys.exit(2)

    # 4. Arreglo rápido de variables si se solicitó
    if args.fix_env:
        ok, msg = doctor.fix_env()
        color = Colors.GREEN if ok else Colors.RED
        print(f"{color}{msg}{Colors.RESET}")

    # 5. Ejecutar diagnóstico
    doctor.run_all_checks()

    # 6. Salida JSON o Terminal
    if args.json:
        payload = {
            "projectName": doctor.profile.get("projectName"),
            "status": doctor.get_overall_status(),
            "summary": doctor.summary,
            "results": doctor.results,
            "remediations": doctor.remediations
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        doctor.print_terminal_report()

    # 7. Generar reporte Markdown opcional
    if args.report:
        report_path = Path(args.report)
        ok, msg = doctor.generate_markdown_report(report_path)
        color = Colors.GREEN if ok else Colors.RED
        print(f"{color}{msg}{Colors.RESET}")

    # Código de salida: 0 = PASS/WARN, 1 = FAIL
    sys.exit(0 if doctor.get_overall_status() in ("PASS", "WARN") else 1)


if __name__ == "__main__":
    main()
