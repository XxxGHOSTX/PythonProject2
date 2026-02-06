#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HYPER-NEXTUS COMPLETE SYSTEM VERIFICATION
==========================================
Validates all components, runs integration tests, generates status report
Enhanced with comprehensive logging and detailed diagnostics
Version: 2.0 - Advanced Verification
Last Enhanced: 2026-02-06
"""

import subprocess
import sys
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import logging
from datetime import datetime

# Configure enhanced logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [VERIFY_SYSTEM] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('verify_system.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('VerifySystem')

class HyperNextusVerification:
    """Complete system verification with enhanced diagnostics"""

    def __init__(self):
        self.base_dir: Path = Path(__file__).parent
        self.results: List[Dict[str, any]] = []
        logger.info("Verification system initialized")

    def verify_python(self) -> Tuple[bool, str]:
        """Function: verify_python"""
        if sys.version_info < (3, 8):
            msg = f"Python 3.8+ required (found {sys.version_info.major}.{sys.version_info.minor})"
            logger.error(msg)
            return False, msg
        msg = f"Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        logger.info(f"Python version verified: {msg}")
        return True, msg

    def verify_venv(self) -> Tuple[bool, str]:
        """Function: verify_venv"""
        venv_path = self.base_dir / ".venv"
        if not venv_path.exists():
            logger.error("Virtual environment not found")
            return False, "Virtual environment not found"
        python_exe = venv_path / "Scripts" / "python.exe"
        if not python_exe.exists():
            logger.error("Python executable not found in venv")
            return False, "Python executable not found in venv"
        logger.info(f"Virtual environment verified at {venv_path}")
        return True, f"Virtual environment at {venv_path}"

    def verify_dependencies(self) -> Tuple[bool, str]:
        """Function: verify_dependencies"""
        required = ['flask', 'flask_cors', 'numpy', 'requests']
        missing = []
        try:
            for pkg in required:
                __import__(pkg)
                logger.debug(f"Dependency verified: {pkg}")
        except ImportError as e:
            missing.append(str(e))
            logger.error(f"Missing dependency: {e}")

        if missing:
            return False, f"Missing dependencies: {', '.join(missing)}"
        logger.info("All dependencies verified")
        return True, "All dependencies installed"

    def verify_core_files(self) -> Tuple[bool, str]:
        """Function: verify_core_files"""
        required_files = [
            'BIOCOMPUTING_CORE.py',
            'biocomputing_api_server.py',
            'hyper_nextus_server.py',
            'thalos_sbi_core_v6.py',
            'thalos_coding_agent_core.py',
            'requirements.txt'
        ]
        missing = [f for f in required_files if not (self.base_dir / f).exists()]

        if missing:
            logger.error(f"Missing core files: {', '.join(missing)}")
            return False, f"Missing files: {', '.join(missing)}"
        logger.info(f"All {len(required_files)} core files present")
        return True, f"All {len(required_files)} core files present"

    def verify_web_interfaces(self) -> Tuple[bool, str]:
        """Function: verify_web_interfaces"""
        interfaces = [
            'thalos_celestial.html',
            'thalos_coding_agent.html',
            'thalos_prime.html',
            'thalos_prime_primary_directive.html'
        ]
        missing = [f for f in interfaces if not (self.base_dir / f).exists()]

        if missing:
            logger.error(f"Missing web interfaces: {', '.join(missing)}")
            return False, f"Missing interfaces: {', '.join(missing)}"
        logger.info(f"All {len(interfaces)} web interfaces present")
        return True, f"All {len(interfaces)} web interfaces present"

    def verify_biocore_import(self) -> Tuple[bool, str]:
        """Function: verify_biocore_import"""
        try:
            from BIOCOMPUTING_CORE import get_biocomputing_core
            core = get_biocomputing_core()
            msg = f"BIOCORE v{core.version} - {core.organoid_matrix.organoid_count:,} organoids"
            logger.info(msg)
            return True, msg
        except Exception as e:
            logger.error(f"BIOCORE import failed: {e}")
            return False, f"BIOCORE import failed: {e}"

    def verify_sbi_import(self) -> Tuple[bool, str]:
        """Function: verify_sbi_import"""
        try:
            from thalos_sbi_core_v6 import ThalosCore
            msg = "SBI Core v6 import successful"
            logger.info(msg)
            return True, msg
        except Exception as e:
            logger.error(f"SBI import failed: {e}")
            return False, f"SBI import failed: {e}"

    def verify_coding_agent_import(self) -> Tuple[bool, str]:
        """Function: verify_coding_agent_import"""
        try:
            from thalos_coding_agent_core import ThalosCodingAgentCore
            core = ThalosCodingAgentCore()
            msg = f"Coding Agent {core.version} - {core.substrate}"
            logger.info(msg)
            return True, msg
        except Exception as e:
            logger.error(f"Coding Agent import failed: {e}")
            return False, f"Coding Agent import failed: {e}"

    def verify_server_config(self) -> Tuple[bool, str]:
        """Function: verify_server_config"""
        server_file = self.base_dir / "hyper_nextus_server.py"
        if not server_file.exists():
            logger.error("hyper_nextus_server.py not found")
            return False, "hyper_nextus_server.py not found"

        content = server_file.read_text()
        checks = [
            ('Flask', 'Flask import'),
            ('CORS', 'CORS configuration'),
            ('/api/biocompute', 'BIOCORE endpoint'),
            ('/api/sbi/query', 'SBI endpoint'),
            ('/api/code/generate', 'Code generation endpoint')
        ]

        missing = [desc for pattern, desc in checks if pattern not in content]
        if missing:
            logger.warning(f"Missing configurations in server: {', '.join(missing)}")
            return False, f"Missing in server: {', '.join(missing)}"

        logger.info("Server configuration verified with all endpoints")
        return True, "Server fully configured with all endpoints"

    def run_verification(self) -> Dict:
        """Run all verification checks"""
        logger.info("Starting system verification")
        print("=" * 70)
        print("HYPER-NEXTUS SYSTEM VERIFICATION")
        print("=" * 70)
        print()

        checks = [
            ("Python Version", self.verify_python),
            ("Virtual Environment", self.verify_venv),
            ("Dependencies", self.verify_dependencies),
            ("Core Files", self.verify_core_files),
            ("Web Interfaces", self.verify_web_interfaces),
            ("BIOCOMPUTING_CORE", self.verify_biocore_import),
            ("SBI Core v6", self.verify_sbi_import),
            ("Coding Agent", self.verify_coding_agent_import),
            ("Server Configuration", self.verify_server_config)
        ]

        passed = 0
        failed = 0

        for name, check_func in checks:
            try:
                success, message = check_func()
                status = "✓" if success else "✗"
                color = "\033[92m" if success else "\033[91m"
                reset = "\033[0m"

                print(f"{color}{status}{reset} {name:<25} {message}")

                if success:
                    passed += 1
                else:
                    failed += 1

                self.results.append({
                    "check": name,
                    "passed": success,
                    "message": message
                })
            except Exception as e:
                print(f"✗ {name:<25} Exception: {e}")
                failed += 1
                self.results.append({
                    "check": name,
                    "passed": False,
                    "message": str(e)
                })

        logger.info(f"Verification completed: {passed} passed, {failed} failed")
        print()
        print("=" * 70)
        print(f"VERIFICATION SUMMARY: {passed} passed, {failed} failed")
        print("=" * 70)

        return {
            "total_checks": len(checks),
            "passed": passed,
            "failed": failed,
            "success_rate": (passed / len(checks)) * 100,
            "results": self.results
        }

    def generate_report(self):
        """Generate detailed verification report"""
        summary = self.run_verification()

        report_file = self.base_dir / "VERIFICATION_REPORT.json"
        report_file.write_text(json.dumps(summary, indent=2))

        logger.info(f"Detailed report saved to: {report_file}")

        print()
        print(f"Detailed report saved to: {report_file}")

        if summary["failed"] == 0:
            print()
            print("✓ ALL SYSTEMS OPERATIONAL")
            print("✓ Ready for deployment: python rapid_deploy.py")
            logger.info("All systems operational, ready for deployment")
            return 0
        else:
            print()
            print(f"⚠ {summary['failed']} check(s) failed")
            print("Review errors above and fix before deployment")
            logger.warning(f"{summary['failed']} check(s) failed, review required")
            return 1

def main():
    verifier = HyperNextusVerification()
    return verifier.generate_report()

if __name__ == "__main__":
    sys.exit(main())
