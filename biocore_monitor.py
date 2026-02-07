# -*- coding: utf-8 -*-
"""
THALOS PRIME - BIOCOMPUTING_CORE Monitor & Manager
==================================================

This tool monitors and manages the BIOCOMPUTING_CORE API server, providing:
- Real-time status monitoring
- Automatic health checks
- Manual reset capability
- Performance metrics
- Error tracking

Enhanced with advanced logging, type safety, and continuous monitoring
Version: 2.0 - Advanced Monitoring
Last Enhanced: 2026-02-06

Usage:
    python biocore_monitor.py              # Monitor mode
    python biocore_monitor.py --reset      # Reset biocore
    python biocore_monitor.py --dashboard  # Interactive dashboard
"""

import logging
import sys
import time
from datetime import datetime
from typing import Any, Dict, Optional

import requests

# CONSTANTS
DEFAULT_BASE_URL: str = "http://localhost:5001"
DEFAULT_TIMEOUT: int = 5
RESET_TIMEOUT: int = 10

# Configure enhanced logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [BIOCORE_MONITOR] %(levelname)s: %(message)s",
    handlers=[logging.FileHandler("biocore_monitor.log"), logging.StreamHandler()],
)
logger = logging.getLogger("BiocoreMonitor")


class BiocoreMonitor:
    """Monitor and manage BIOCOMPUTING_CORE API server with enhanced capabilities."""

    def __init__(self, base_url: str = DEFAULT_BASE_URL):
        self.base_url: str = base_url
        self.last_status: Optional[Dict[str, Any]] = None
        logger.info(f"BiocoreMonitor initialized for {base_url}")

    def check_health(self) -> bool:
        """Function: check_health"""
        try:
            response = requests.get(f"{self.base_url}/api/health", timeout=DEFAULT_TIMEOUT)
            is_healthy = response.status_code == 200
            if not is_healthy:
                logger.warning(f"Health check failed: status code {response.status_code}")
            return is_healthy
        except Exception as e:
            logger.error(f"Health check error: {e}")
            return False

    def get_status(self) -> Optional[Dict[str, Any]]:
        """Function: get_status"""
        try:
            response = requests.get(f"{self.base_url}/api/status", timeout=DEFAULT_TIMEOUT)
            if response.status_code == 200:
                status = response.json()
                self.last_status = status
                return status
            logger.warning(f"Status request failed: {response.status_code}")
            return None
        except Exception as e:
            logger.error(f"Status request error: {e}")
            return None

    def reset_biocore(self, reason: str = "Manual reset from monitor") -> bool:
        """Function: reset_biocore"""
        logger.info(f"Initiating biocore reset: {reason}")
        try:
            response = requests.post(
                f"{self.base_url}/api/reset", json={"reason": reason}, timeout=RESET_TIMEOUT
            )
            success = response.status_code == 200
            if success:
                logger.info("Biocore reset successful")
            else:
                logger.error(f"Reset failed: {response.status_code}")
            return success
        except Exception as e:
            logger.error(f"Reset error: {e}")
            return False

    def send_test_query(self, query: str = "What is a black hole?") -> Optional[Dict[str, Any]]:
        """Send test query to biocore."""
        try:
            response = requests.post(
                f"{self.base_url}/api/biocompute", json={"query": query}, timeout=30
            )
            if response.status_code == 200:
                return response.json()
            return None
        except requests.RequestException:
            return None

    def print_status(self, status: Dict[str, Any]):
        """Print formatted status information."""
        print("\n" + "=" * 80)
        print("BIOCOMPUTING_CORE STATUS")
        print("=" * 80)

        # Server health
        health = status.get("server_health", {})
        print("\nServer Health:")
        print(f"  Request Count: {health.get('request_count', 0)}")
        print(f"  Error Count: {health.get('error_count', 0)}")
        print(f"  Uptime: {health.get('time_since_reset_seconds', 0):.2f}s")
        print(f"  Next Auto-Reset: {health.get('time_until_auto_reset_seconds', 0):.2f}s")

        # Biocore info
        biocore = status.get("biocomputing_core", {})
        print("\nBiocomputing Core:")
        print(f"  Version: {biocore.get('version', 'Unknown')}")
        print(f"  Organoid Count: {biocore.get('organoid_count', 0):,}")
        print(f"  Total Queries: {biocore.get('total_queries', 0)}")
        print(f"  Avg Processing Time: {biocore.get('avg_processing_time_ms', 0):.2f}ms")

        # Configuration
        print("\nAuto-Reset Configuration:")
        print(f"  Interval: {health.get('auto_reset_interval', 0)}s")
        print(f"  Error Threshold: {health.get('error_threshold', 0)}")
        print(f"  Request Limit: {health.get('request_limit_per_hour', 0)}/hour")

        print("=" * 80)

    def monitor_loop(self, interval: int = 10):
        """Continuous monitoring loop."""
        print("Starting BIOCOMPUTING_CORE monitor...")
        print(f"Server: {self.base_url}")
        print(f"Refresh interval: {interval}s")
        print("Press CTRL+C to stop\n")

        try:
            while True:
                is_healthy = self.check_health()

                if is_healthy:
                    status = self.get_status()
                    if status:
                        self.print_status(status)
                        self.last_status = status
                    else:
                        print(f"\n[{datetime.now()}] WARNING: Status endpoint failed")
                else:
                    print(f"\n[{datetime.now()}] ERROR: Server is not responding!")
                    print("  - Check if server is running")
                    print("  - Run: python biocomputing_api_server.py --port 5001")

                time.sleep(interval)

        except KeyboardInterrupt:
            print("\n\nMonitor stopped by user")

    def interactive_dashboard(self):
        """Interactive dashboard with menu."""
        while True:
            print("\n" + "=" * 80)
            print("THALOS PRIME - BIOCOMPUTING_CORE Dashboard")
            print("=" * 80)
            print("\nOptions:")
            print("  1. Check Status")
            print("  2. Check Health")
            print("  3. Send Test Query")
            print("  4. Reset Biocore")
            print("  5. Start Monitoring (10s refresh)")
            print("  6. Exit")
            print()

            choice = input("Select option (1-6): ").strip()

            if choice == "1":
                print("\nFetching status...")
                status = self.get_status()
                if status:
                    self.print_status(status)
                else:
                    print("ERROR: Could not fetch status")

            elif choice == "2":
                print("\nChecking health...")
                is_healthy = self.check_health()
                if is_healthy:
                    print("✓ Server is HEALTHY")
                else:
                    print("✗ Server is DOWN or UNREACHABLE")

            elif choice == "3":
                query = input("\nEnter test query (or press Enter for default): ").strip()
                if not query:
                    query = "What is a black hole?"

                print(f"\nSending query: {query}")
                result = self.send_test_query(query)

                if result:
                    print(f"\nStatus: {result.get('status')}")
                    response = result.get("response", {})
                    print(f"Domain: {response.get('domain')}")
                    print(f"Confidence: {response.get('confidence', 0):.0%}")
                    print(f"Processing Time: {response.get('processing_time_ms', 0):.2f}ms")
                    print("\nResponse (first 200 chars):")
                    print(response.get("text", "")[:200] + "...")
                else:
                    print("ERROR: Query failed")

            elif choice == "4":
                confirm = (
                    input("\nAre you sure you want to reset biocore? (yes/no): ").strip().lower()
                )
                if confirm == "yes":
                    reason = (
                        input("Reason for reset (optional): ").strip()
                        or "Manual reset from dashboard"
                    )
                    print("\nResetting biocore...")
                    success = self.reset_biocore(reason)
                    if success:
                        print("✓ Biocore reset successfully")
                    else:
                        print("✗ Reset failed")
                else:
                    print("Reset cancelled")

            elif choice == "5":
                self.monitor_loop()

            elif choice == "6":
                print("\nExiting dashboard...")
                break

            else:
                print("\nInvalid option, please try again")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="BIOCOMPUTING_CORE Monitor & Manager")
    parser.add_argument("--url", type=str, default="http://localhost:5001", help="Biocore API URL")
    parser.add_argument("--monitor", action="store_true", help="Start monitoring mode")
    parser.add_argument("--interval", type=int, default=10, help="Monitoring interval (seconds)")
    parser.add_argument("--reset", action="store_true", help="Reset biocore and exit")
    parser.add_argument("--test", action="store_true", help="Send test query and exit")
    parser.add_argument("--dashboard", action="store_true", help="Interactive dashboard")

    args = parser.parse_args()

    monitor = BiocoreMonitor(args.url)

    if args.reset:
        print("Resetting BIOCOMPUTING_CORE...")
        success = monitor.reset_biocore("Reset via command line")
        if success:
            print("✓ Reset successful")
            sys.exit(0)
        else:
            print("✗ Reset failed")
            sys.exit(1)

    elif args.test:
        print("Sending test query...")
        result = monitor.send_test_query()
        if result:
            print("✓ Test successful")
            print(f"  Domain: {result.get('response', {}).get('domain')}")
            print(f"  Confidence: {result.get('response', {}).get('confidence', 0):.0%}")
            sys.exit(0)
        else:
            print("✗ Test failed")
            sys.exit(1)

    elif args.monitor:
        monitor.monitor_loop(args.interval)

    elif args.dashboard:
        monitor.interactive_dashboard()

    else:
        # Default: check status once
        print("Checking BIOCOMPUTING_CORE status...")
        status = monitor.get_status()
        if status:
            monitor.print_status(status)
        else:
            print("ERROR: Could not connect to server")
            print(f"Make sure server is running at: {args.url}")
            print("\nStart server with:")
            print("  python biocomputing_api_server.py --port 5001")
            sys.exit(1)


if __name__ == "__main__":
    main()
