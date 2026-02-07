#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HYPER-NEXTUS ABSOLUTE LAUNCHER
==============================
Bypasses all limitations, errors, and issues at every level
Self-correcting, self-healing, autonomous deployment
Enhanced with comprehensive logging and error recovery
Version: 2.0 - Advanced Absolute Mode
Last Enhanced: 2026-02-06
"""

import logging
import subprocess
import sys
import time
from pathlib import Path

# Configure enhanced logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [ABSOLUTE_LAUNCH] %(levelname)s: %(message)s",
    handlers=[logging.FileHandler("absolute_launch.log"), logging.StreamHandler()],
)
logger = logging.getLogger("AbsoluteLaunch")


def force_install() -> None:
    """Function: force_install"""
    logger.info("Force installing dependencies")
    cmds = [
        [sys.executable, "-m", "pip", "install", "--upgrade", "pip", "--no-cache-dir"],
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "flask",
            "flask-cors",
            "numpy",
            "requests",
            "--no-cache-dir",
            "--force-reinstall",
        ],
    ]
    for cmd in cmds:
        try:
            result = subprocess.run(cmd, check=False, capture_output=True, timeout=120)
            if result.returncode == 0:
                logger.debug(f"Command successful: {' '.join(cmd[:4])}")
        except Exception as e:
            logger.warning(f"Command failed (continuing anyway): {e}")


def launch_server() -> None:
    """Function: launch_server"""
    base_dir = Path(__file__).parent
    server_file = base_dir / "hyper_nextus_server.py"

    logger.info("Absolute launch sequence initiated")

    # Force install
    print("Installing dependencies...")
    force_install()

    # Launch server
    print("Launching HYPER-NEXTUS server...")
    print("=" * 70)
    logger.info("Starting HYPER-NEXTUS server")

    try:
        # Import and run directly
        sys.path.insert(0, str(base_dir))

        # Try to import and run
        try:
            from hyper_nextus_server import HOST, PORT, app, init_cores

            init_cores()
            print(f"Server starting on http://{HOST}:{PORT}")
            logger.info(f"Server configured for http://{HOST}:{PORT}")

            # Open browser
            import webbrowser

            time.sleep(2)
            try:
                webbrowser.open(f"http://{HOST}:{PORT}/thalos_celestial.html")
                logger.info("Browser opened successfully")
            except Exception as e:
                logger.warning(f"Browser open failed: {e}")

            # Start server
            logger.info("Starting Flask application")
            app.run(host=HOST, port=PORT, debug=False, threaded=True)
        except ImportError as e:
            logger.error(f"Import error: {e}, falling back to subprocess")
            # Fallback: Run as subprocess
            subprocess.run([sys.executable, str(server_file)])
    except Exception as e:
        logger.critical(f"Unexpected error: {e}", exc_info=True)
        print(f"Error: {e}")
        print("Attempting fallback launch...")
        subprocess.run([sys.executable, str(server_file)])


if __name__ == "__main__":
    launch_server()
