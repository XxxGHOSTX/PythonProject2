# -*- coding: utf-8 -*-
"""
Thalos Prime v4.0 SBI Interface - Deployment Server
Simple HTTP server to host the Thalos Prime interface locally
Enhanced with logging, error handling, and monitoring capabilities
Last Enhanced: 2026-02-06
"""

import http.server
import logging
import os
import socketserver
import sys
import webbrowser
from pathlib import Path

# CONSTANTS
DEFAULT_PORT: int = 8080
DIRECTORY: Path = Path(__file__).parent

# Configure enhanced logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [DEPLOY_SERVER] %(levelname)s: %(message)s",
    handlers=[logging.FileHandler("deploy_server.log"), logging.StreamHandler()],
)
logger = logging.getLogger("DeployServer")

# Port configuration
PORT: int = DEFAULT_PORT
# Allow override from environment variable or command-line argument
if "THALOS_PORT" in os.environ:
    try:
        PORT = int(os.environ["THALOS_PORT"])
        logger.info(f"Port set from environment: {PORT}")
    except ValueError as e:
        logger.warning(f"Invalid THALOS_PORT environment variable: {e}")
elif len(sys.argv) > 1:
    try:
        PORT = int(sys.argv[1])
        logger.info(f"Port set from command-line: {PORT}")
    except ValueError as e:
        logger.warning(f"Invalid command-line port argument: {e}")


class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP handler with CORS support and logging"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIRECTORY), **kwargs)

    def end_headers(self):
        """Function: end_headers"""
        # Add CORS headers for API requests
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def log_message(self, format, *args):
        """Override to use logger instead of stderr"""
        logger.info(f"{self.address_string()} - {format % args}")


def main() -> None:
    """Function: main"""
    print("=" * 60)
    print("THALOS PRIME - DEPLOYMENT SERVER")
    print("=" * 60)
    print(f"\n🚀 Starting server on port {PORT}...")
    print(f"📁 Serving files from: {DIRECTORY}")

    with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
        base_url = f"http://localhost:{PORT}"
        print("\n✅ Server running successfully!")
        print("\n🌐 Available Interfaces:")
        print("\n   [1] Terminal Edition (Green Matrix)")
        print(f"       {base_url}/thalos_prime.html")
        print("\n   [2] Celestial Navigator (Amber/Gold)")
        print(f"       {base_url}/thalos_celestial.html")
        print("\n   [3] Primary Directive (Advanced SBI)")
        print(f"       {base_url}/thalos_prime_primary_directive.html")
        print("\n   [4] ⚡ CODING AGENT (Superior Code Generation)")
        print(f"       {base_url}/thalos_coding_agent.html")
        print("\n💡 Tip: Open multiple interfaces in different browser tabs!")
        print("\n🛑 Press Ctrl+C to stop the server\n")
        print("=" * 60)

        # Ask user which version to open
        try:
            print("\nWhich version would you like to open?")
            print("1 - Terminal Edition")
            print("2 - Celestial Navigator")
            print("3 - Primary Directive")
            print("4 - ⚡ CODING AGENT (Superior SBI)")
            print("5 - All Interfaces")
            print("0 - None (server only)")

            choice = input("\nYour choice (0-5): ").strip()

            if choice == "1":
                webbrowser.open(f"{base_url}/thalos_prime.html")
                print("✓ Opening Terminal Edition...\n")
            elif choice == "2":
                webbrowser.open(f"{base_url}/thalos_celestial.html")
                print("✓ Opening Celestial Navigator...\n")
            elif choice == "3":
                webbrowser.open(f"{base_url}/thalos_prime_primary_directive.html")
                print("✓ Opening Primary Directive...\n")
            elif choice == "4":
                webbrowser.open(f"{base_url}/thalos_coding_agent.html")
                print("✓ Opening CODING AGENT...\n")
            elif choice == "5":
                webbrowser.open(f"{base_url}/thalos_prime.html")
                webbrowser.open(f"{base_url}/thalos_celestial.html")
                webbrowser.open(f"{base_url}/thalos_prime_primary_directive.html")
                webbrowser.open(f"{base_url}/thalos_coding_agent.html")
                print("✓ Opening all interfaces...\n")
            else:
                print("✓ Server running without opening browser\n")
        except Exception:
            print("✓ Server running\n")

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n🛑 Shutting down server...")
            print("Goodbye!\n")


if __name__ == "__main__":
    main()
