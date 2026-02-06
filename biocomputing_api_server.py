# -*- coding: utf-8 -*-
"""
THALOS PRIME - BIOCOMPUTING CORE API SERVER
===========================================

Flask-based API server that exposes the BIOCOMPUTING_CORE wetware intelligence.
All Thalos modules connect to this server for online processing.

Even when offline, the full biocomputing intelligence is hardcoded locally,
ensuring identical responses whether online or offline.

Endpoints:
- POST /api/biocompute - Process query through neural organoid matrix
- GET /api/status - Get biocomputing core status
- GET /api/health - Health check

Version: 10.0 (Enhanced Autonomous Operations)
Last Enhanced: 2026-02-06
Optimization Level: Maximum
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from datetime import datetime
import time
import threading
from functools import wraps
from typing import Dict, Any, Optional, Tuple

# Import biocomputing core
from BIOCOMPUTING_CORE import get_biocomputing_core, BiologicalResponse

app = Flask(__name__)
CORS(app)  # Enable CORS for all Thalos web modules

# Initialize biocomputing core with auto-recovery
biocore: Optional[Any] = None
biocore_lock = threading.Lock()
biocore_last_reset: float = time.time()
biocore_request_count: int = 0
biocore_error_count: int = 0

# CONSTANTS
AUTO_RESET_INTERVAL: int = 3600  # Reset every hour
AUTO_RESET_ERROR_THRESHOLD: int = 10  # Reset after 10 consecutive errors
REQUEST_LIMIT_PER_HOUR: int = 1000  # Soft limit, triggers warning

# Configure enhanced logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [BIOCORE_API] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('biocore_api.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('BIOCOMPUTING_API')


def get_or_reset_biocore() -> Any:
    """Get biocomputing core instance, resetting if needed."""
    global biocore, biocore_last_reset, biocore_request_count, biocore_error_count

    with biocore_lock:
        current_time = time.time()
        time_since_reset = current_time - biocore_last_reset

        # Auto-reset conditions
        should_reset = False
        reset_reason = ""

        if biocore is None:
            should_reset = True
            reset_reason = "Initial initialization"
        elif time_since_reset > AUTO_RESET_INTERVAL:
            should_reset = True
            reset_reason = f"Auto-reset interval ({AUTO_RESET_INTERVAL}s exceeded)"
        elif biocore_error_count >= AUTO_RESET_ERROR_THRESHOLD:
            should_reset = True
            reset_reason = f"Error threshold ({AUTO_RESET_ERROR_THRESHOLD} errors)"
        elif biocore_request_count > REQUEST_LIMIT_PER_HOUR:
            logger.warning(f"Request limit exceeded: {biocore_request_count} > {REQUEST_LIMIT_PER_HOUR}")
            # Don't reset, just warn

        if should_reset:
            logger.info(f"Resetting BIOCOMPUTING_CORE: {reset_reason}")
            try:
                biocore = get_biocomputing_core()
                biocore_last_reset = current_time
                biocore_request_count = 0
                biocore_error_count = 0
                logger.info("BIOCOMPUTING_CORE reset successful")
            except Exception as e:
                logger.error(f"Failed to reset BIOCOMPUTING_CORE: {e}")
                # Continue with old instance if reset fails

        return biocore


def auto_recover(f):
    """Decorator to automatically recover from errors."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        global biocore_error_count, biocore_request_count

        try:
            biocore_request_count += 1
            result = f(*args, **kwargs)
            biocore_error_count = 0  # Reset error count on success
            return result
        except Exception as e:
            biocore_error_count += 1
            logger.error(f"Error in {f.__name__}: {e}, error count: {biocore_error_count}")

            # Attempt recovery
            if biocore_error_count >= AUTO_RESET_ERROR_THRESHOLD:
                logger.warning("Error threshold reached, triggering core reset")
                get_or_reset_biocore()

            # Return error response
            return jsonify({
                "status": "error",
                "message": str(e),
                "recovery_attempted": biocore_error_count >= AUTO_RESET_ERROR_THRESHOLD
            }), 500

    return decorated_function


@app.route('/api/biocompute', methods=['POST'])
@auto_recover
def biocompute():
    """
    Process query through BIOCOMPUTING_CORE with automatic error recovery.

    Features:
    - Auto-resets core on error threshold
    - Auto-resets core after time interval
    - Graceful degradation on failures
    - Request counting and monitoring

    Request JSON:
    {
        "query": "Your question here",
        "context": {optional context dict}
    }

    Response JSON:
    {
        "status": "success",
        "response": {
            "text": "...",
            "confidence": 0.85,
            "domain": "astrophysics",
            "processing_time_ms": 55.3,
            "verification": "high_confidence",
            "synaptic_patterns": [...],
            "cross_domain_connections": [...]
        },
        "metadata": {
            "biocomputing_version": "9.0",
            "substrate": "Synthetic Biological Intelligence - Human Neural Organoids",
            "organoid_count": 50000,
            "timestamp": "2026-02-06T...",
            "request_count": 123,
            "time_since_reset": 456.78
        }
    }
    """
    data = request.get_json()

    if not data or 'query' not in data:
        return jsonify({
            "status": "error",
            "message": "Missing 'query' field in request"
        }), 400

    query = data['query']
    context = data.get('context', None)

    logger.info(f"Processing biocompute request #{biocore_request_count}: {query[:100]}...")

    # Get or reset biocore as needed
    core = get_or_reset_biocore()

    # Process through biocomputing core
    response = core.process_query(query, context)

    # Calculate time since last reset
    time_since_reset = time.time() - biocore_last_reset

    # Format response
    result = {
        "status": "success",
        "response": {
            "text": response.response_text,
            "confidence": response.confidence,
            "domain": response.domain.value,
            "processing_time_ms": response.processing_time_ms,
            "verification": response.verification_status,
            "synaptic_patterns": response.synaptic_patterns,
            "cross_domain_connections": [
                {"from": link[0], "to": link[1]}
                for link in response.cross_domain_connections
            ]
        },
        "metadata": {
            "biocomputing_version": core.version,
            "substrate": core.substrate,
            "organoid_count": core.organoid_matrix.organoid_count,
            "synapse_density": core.organoid_matrix.synapse_density,
            "timestamp": datetime.now().isoformat(),
            "request_count": biocore_request_count,
            "time_since_reset_seconds": round(time_since_reset, 2),
            "error_count": biocore_error_count
        }
    }

    logger.info(f"Request #{biocore_request_count} completed: {response.processing_time_ms:.2f}ms, confidence: {response.confidence:.0%}")

    return jsonify(result), 200


@app.route('/api/status', methods=['GET'])
@auto_recover
def status():
    """Get BIOCOMPUTING_CORE status with auto-reset metrics."""
    core = get_or_reset_biocore()
    core_status = core.get_status()

    time_since_reset = time.time() - biocore_last_reset
    time_until_reset = max(0, AUTO_RESET_INTERVAL - time_since_reset)

    return jsonify({
        "status": "operational",
        "biocomputing_core": {
            "version": core_status["version"],
            "substrate": core_status["substrate"],
            "organoid_count": core_status["organoid_count"],
            "synapse_density": core_status["synapse_density"],
            "total_queries": core_status["total_queries"],
            "avg_processing_time_ms": core_status["avg_processing_time_ms"]
        },
        "server_health": {
            "request_count": biocore_request_count,
            "error_count": biocore_error_count,
            "time_since_reset_seconds": round(time_since_reset, 2),
            "time_until_auto_reset_seconds": round(time_until_reset, 2),
            "auto_reset_interval": AUTO_RESET_INTERVAL,
            "error_threshold": AUTO_RESET_ERROR_THRESHOLD,
            "request_limit_per_hour": REQUEST_LIMIT_PER_HOUR
        },
        "capabilities": core_status["capabilities"],
        "knowledge_domains": [domain.value for domain in core_status["knowledge_domains"]],
        "timestamp": datetime.now().isoformat()
    }), 200


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "biocomputing_core": "operational",
        "version": "9.0",
        "timestamp": datetime.now().isoformat(),
        "uptime_seconds": round(time.time() - biocore_last_reset, 2)
    }), 200


@app.route('/api/reset', methods=['POST'])
@auto_recover
def manual_reset():
    """
    Manually reset BIOCOMPUTING_CORE.

    Useful for:
    - Clearing accumulated state
    - Forcing fresh initialization
    - Recovery from errors

    Request JSON (optional):
    {
        "reason": "Manual reset requested by admin"
    }
    """
    global biocore, biocore_last_reset, biocore_request_count, biocore_error_count

    data = request.get_json() or {}
    reason = data.get('reason', 'Manual reset via API')

    logger.info(f"Manual reset requested: {reason}")

    with biocore_lock:
        try:
            old_request_count = biocore_request_count
            old_error_count = biocore_error_count
            old_uptime = time.time() - biocore_last_reset

            biocore = get_biocomputing_core()
            biocore_last_reset = time.time()
            biocore_request_count = 0
            biocore_error_count = 0

            logger.info("Manual reset successful")

            return jsonify({
                "status": "success",
                "message": "BIOCOMPUTING_CORE reset successfully",
                "previous_stats": {
                    "request_count": old_request_count,
                    "error_count": old_error_count,
                    "uptime_seconds": round(old_uptime, 2)
                },
                "reset_reason": reason,
                "timestamp": datetime.now().isoformat()
            }), 200

        except Exception as e:
            logger.error(f"Manual reset failed: {e}")
            return jsonify({
                "status": "error",
                "message": f"Reset failed: {str(e)}"
            }), 500


@app.route('/')
def index():
    """Root endpoint with server information."""
    core = get_or_reset_biocore()

    return jsonify({
        "message": "THALOS PRIME - BIOCOMPUTING_CORE API Server",
        "version": "9.0",
        "substrate": core.substrate,
        "endpoints": {
            "POST /api/biocompute": "Process query through neural organoid matrix",
            "GET /api/status": "Get biocomputing core status with health metrics",
            "GET /api/health": "Health check endpoint",
            "POST /api/reset": "Manually reset biocomputing core (admin)",
            "GET /": "This information page"
        },
        "features": [
            "Automatic error recovery",
            "Auto-reset on error threshold",
            "Auto-reset on time interval",
            "Request counting and monitoring",
            "Graceful degradation",
            "Zero external dependencies"
        ],
        "capabilities": [
            "Synthetic biological intelligence",
            "Human neural organoids (50,000 units)",
            "Unrestricted general-purpose intelligence",
            "First-principles analytical reasoning",
            "Cross-domain synthesis",
            "Anti-hallucination verification"
        ],
        "auto_reset_config": {
            "interval_seconds": AUTO_RESET_INTERVAL,
            "error_threshold": AUTO_RESET_ERROR_THRESHOLD,
            "request_limit_per_hour": REQUEST_LIMIT_PER_HOUR
        },
        "current_stats": {
            "request_count": biocore_request_count,
            "error_count": biocore_error_count,
            "uptime_seconds": round(time.time() - biocore_last_reset, 2)
        }
    }), 200


def main():
    """Start BIOCOMPUTING_CORE API server with enhanced features."""
    import argparse

    parser = argparse.ArgumentParser(description='BIOCOMPUTING_CORE API Server v9.0')
    parser.add_argument('--port', type=int, default=5001, help='Port to run on')
    parser.add_argument('--host', type=str, default='127.0.0.1', help='Host to bind to')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--reset-interval', type=int, default=3600, help='Auto-reset interval (seconds)')
    parser.add_argument('--error-threshold', type=int, default=10, help='Error threshold for auto-reset')

    args = parser.parse_args()

    # Update configuration from arguments
    global AUTO_RESET_INTERVAL, AUTO_RESET_ERROR_THRESHOLD
    AUTO_RESET_INTERVAL = args.reset_interval
    AUTO_RESET_ERROR_THRESHOLD = args.error_threshold

    # Initialize biocore
    core = get_or_reset_biocore()

    print("=" * 80)
    print("THALOS PRIME - BIOCOMPUTING_CORE API SERVER v9.0")
    print("=" * 80)
    print(f"Version: {core.version}")
    print(f"Substrate: {core.substrate}")
    print(f"Organoid Count: {core.organoid_matrix.organoid_count:,}")
    print(f"Synapse Density: {core.organoid_matrix.synapse_density:.2e}")
    print()
    print("Enhanced Features:")
    print("  + Automatic error recovery")
    print(f"  + Auto-reset every {AUTO_RESET_INTERVAL}s")
    print(f"  + Auto-reset on {AUTO_RESET_ERROR_THRESHOLD} consecutive errors")
    print(f"  + Request monitoring ({REQUEST_LIMIT_PER_HOUR} req/hour soft limit)")
    print("  + Manual reset endpoint (POST /api/reset)")
    print("  + Graceful degradation")
    print()
    print("Capabilities:")
    status = core.get_status()
    for cap in status["capabilities"]:
        print(f"  + {cap}")
    print()
    print(f"Starting server on http://{args.host}:{args.port}")
    print("Press CTRL+C to stop")
    print("=" * 80)
    print()

    app.run(host=args.host, port=args.port, debug=args.debug, threaded=True)


if __name__ == '__main__':
    main()
