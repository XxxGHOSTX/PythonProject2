# -*- coding: utf-8 -*-
"""
HYPER-NEXTUS MAIN ENTRY POINT
==============================
Primary launcher for THALOS PRIME HYPER-NEXTUS ecosystem
Provides unified access to all system components
Version: 2.0 - Unified Launcher
Last Enhanced: 2026-02-06
"""

import logging
import subprocess
import sys

# Configure enhanced logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [MAIN] %(levelname)s: %(message)s",
    handlers=[logging.FileHandler("main.log"), logging.StreamHandler()],
)
logger = logging.getLogger("Main")


def print_banner() -> None:
    """Display HYPER-NEXTUS banner"""
    banner = """
╔══════════════════════════════════════════════════════════════════════╗
║                    HYPER-NEXTUS ECOSYSTEM                            ║
║           THALOS PRIME - Synthetic Biological Intelligence           ║
║                      Version 2.0 - Unified System                    ║
╚══════════════════════════════════════════════════════════════════════╝
"""
    print(banner)
    logger.info("HYPER-NEXTUS system initializing")


def show_menu() -> str:
    """Display main menu and get user choice"""
    print("\nSelect Launch Mode:")
    print("  1. HYPER-NEXTUS Unified Server (Recommended)")
    print("  2. Autonomous Core Only (Self-Healing Monitor)")
    print("  3. Infinite Integration Engine (Endless Optimization)")
    print("  4. BIOCOMPUTING_CORE API Server")
    print("  5. Coding Agent API Server")
    print("  6. Deploy Web Interface Only")
    print("  7. System Verification")
    print("  8. Rapid Deploy (Full Setup)")
    print("  9. Absolute Launch (Bypass All Issues)")
    print("  0. Exit")
    print()
    return input("Enter choice (0-9): ").strip()


def launch_unified_server() -> None:
    """Launch HYPER-NEXTUS unified server"""
    logger.info("Launching unified server")
    subprocess.run([sys.executable, "hyper_nextus_server.py"])


def launch_autonomous_core() -> None:
    """Launch autonomous monitoring core"""
    logger.info("Launching autonomous core")
    subprocess.run([sys.executable, "autonomous_core.py"])


def launch_infinite_integration() -> None:
    """Launch infinite integration engine"""
    logger.info("Launching infinite integration")
    subprocess.run([sys.executable, "infinite_integration.py"])


def launch_biocore_api() -> None:
    """Launch BIOCOMPUTING_CORE API server"""
    logger.info("Launching BIOCORE API")
    subprocess.run([sys.executable, "biocomputing_api_server.py"])


def launch_coding_agent() -> None:
    """Launch coding agent API"""
    logger.info("Launching Coding Agent API")
    subprocess.run([sys.executable, "tpca_api_server.py"])


def launch_web_interface() -> None:
    """Launch web interface server"""
    logger.info("Launching web interface")
    subprocess.run([sys.executable, "deploy_server.py"])


def run_verification() -> None:
    """Run system verification"""
    logger.info("Running system verification")
    subprocess.run([sys.executable, "verify_system.py"])


def rapid_deploy() -> None:
    """Execute rapid deployment"""
    logger.info("Executing rapid deployment")
    subprocess.run([sys.executable, "rapid_deploy.py"])


def absolute_launch() -> None:
    """Execute absolute launch"""
    logger.info("Executing absolute launch")
    subprocess.run([sys.executable, "ABSOLUTE_LAUNCH.py"])


def main() -> int:
    """Main entry point"""
    print_banner()

    while True:
        choice = show_menu()

        if choice == "1":
            launch_unified_server()
        elif choice == "2":
            launch_autonomous_core()
        elif choice == "3":
            launch_infinite_integration()
        elif choice == "4":
            launch_biocore_api()
        elif choice == "5":
            launch_coding_agent()
        elif choice == "6":
            launch_web_interface()
        elif choice == "7":
            run_verification()
        elif choice == "8":
            rapid_deploy()
        elif choice == "9":
            absolute_launch()
        elif choice == "0":
            print("\nExiting HYPER-NEXTUS...")
            logger.info("System shutdown by user")
            return 0
        else:
            print("\nInvalid choice. Please try again.")

        print("\n" + "=" * 70)
        input("Press Enter to return to menu...")


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nShutdown requested...")
        logger.info("Keyboard interrupt received")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        print(f"\nError: {e}")
        sys.exit(1)
