# -*- coding: utf-8 -*-
"""
HYPER-NEXTUS RAPID ACTIVATION SCRIPT
====================================
Production-ready execution with zero configuration required
Enhanced with comprehensive error handling and logging
Version: 2.0 - Enhanced Deployment
Last Enhanced: 2026-02-06
"""

import logging
import subprocess
import sys
from pathlib import Path

# Configure enhanced logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [RAPID_DEPLOY] %(levelname)s: %(message)s",
    handlers=[logging.FileHandler("rapid_deploy.log"), logging.StreamHandler()],
)
logger = logging.getLogger("RapidDeploy")


def main() -> int:
    """Function: main"""
    base_dir = Path(__file__).parent
    logger.info("Rapid deployment initiated")

    print("=" * 70)
    print("HYPER-NEXTUS RAPID ACTIVATION")
    print("=" * 70)
    print()

    # Check Python
    print("[1/3] Verifying Python...")
    if sys.version_info < (3, 8):
        msg = (
            f"ERROR: Python 3.8+ required (found {sys.version_info.major}.{sys.version_info.minor})"
        )
        print(msg)
        logger.error(msg)
        return 1
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    logger.info(
        f"Python version verified: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    )

    # Setup venv
    print("\n[2/3] Setting up environment...")
    venv_path = base_dir / ".venv"
    if not venv_path.exists():
        print("Creating virtual environment...")
        logger.info("Creating virtual environment")
        try:
            subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
            logger.info("Virtual environment created successfully")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to create virtual environment: {e}")
            return 1

    # Activate and install
    python_exe = venv_path / "Scripts" / "python.exe"

    print("Installing dependencies...")
    logger.info("Installing dependencies")
    try:
        subprocess.run(
            [str(python_exe), "-m", "pip", "install", "-q", "--upgrade", "pip"], check=True
        )
        subprocess.run(
            [str(python_exe), "-m", "pip", "install", "-q", "-r", "requirements.txt"], check=True
        )
        print("✓ Environment ready")
        logger.info("Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install dependencies: {e}")
        return 1

    print("\n[3/3] Launching deployment server...")
    logger.info("Launching deploy_server.py")
    try:
        subprocess.run(
            [
                str(python_exe),
                "deploy_server.py",
            ],
            check=True,
            cwd=str(base_dir),
        )
    except KeyboardInterrupt:
        print("\nDeployment cancelled by user.")
        logger.info("Deployment cancelled by user")
        return 0
    except subprocess.CalledProcessError as e:
        logger.error(f"Deployment failed: {e}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
