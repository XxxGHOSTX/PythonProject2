# -*- coding: utf-8 -*-
"""
THALOS PRIME CODING AGENT (TPCA) - API SERVER
=============================================

Flask-based API server that exposes TPCA autonomous core engine.
Provides RESTful endpoints for code generation without external dependencies.

Endpoints:
- POST /api/generate - Generate code from natural language request
- GET /api/status - Get agent status and capabilities
- GET /api/health - Health check endpoint

Author: Thalos Prime Systems
Version: 9.0 (Enhanced Autonomous Operations)
Last Enhanced: 2026-02-06
Optimization Level: Maximum
"""

import logging
import os
import sys

from flask import Flask, jsonify, request
from flask_cors import CORS

# Add parent directory to path to import thalos_coding_agent_core
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from thalos_coding_agent_core import CodeRequest, GenerationMode, ThalosCodingAgentCore

app = Flask(__name__)
CORS(app)  # Enable CORS for web interface

# Initialize TPCA core engine
tpca_core: ThalosCodingAgentCore = ThalosCodingAgentCore()

# CONSTANTS
DEFAULT_PORT: int = 5002
DEFAULT_HOST: str = "127.0.0.1"
DEFAULT_COMPLEXITY: int = 5

# Configure enhanced logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [TPCA_API] %(levelname)s: %(message)s",
    handlers=[logging.FileHandler("tpca_api.log"), logging.StreamHandler()],
)
logger = logging.getLogger("TPCA_API")


@app.route("/api/generate", methods=["POST"])
def generate_code() -> tuple:
    """
    Generate code from natural language request.

    Request JSON:
    {
        "query": "Create a REST API with authentication",
        "mode": "full",  # full, function, class, api, algorithm, debug, optimize, explain
        "language": "python",
        "complexity": 7,  # 1-10
        "files": []  # Optional attached files
    }

    Response JSON:
    {
        "status": "success",
        "artifact": {
            "code": "...",
            "tests": "...",
            "documentation": "...",
            "complexity_analysis": "...",
            "security_notes": "...",
            "run_instructions": "..."
        },
        "metadata": {
            "agent_version": "8.0",
            "substrate": "SBI Wetware-Hybrid Neural Matrix",
            "mode": "autonomous"
        }
    }
    """
    try:
        data = request.get_json()

        # Validate request
        if not data or "query" not in data:
            return jsonify({"status": "error", "message": "Missing 'query' field in request"}), 400

        # Parse mode
        mode_str = data.get("mode", "full").lower()
        try:
            mode = GenerationMode(mode_str)
        except ValueError:
            mode = GenerationMode.FULL_APPLICATION

        # Create request
        code_request = CodeRequest(
            query=data["query"],
            mode=mode,
            language=data.get("language", "python").lower(),
            complexity=int(data.get("complexity", 7)),
            attached_files=data.get("files", []),
        )

        # Generate code using autonomous core
        artifact = tpca_core.generate(code_request)

        # Format response
        response = {
            "status": "success",
            "artifact": {
                "code": artifact.code,
                "tests": artifact.tests,
                "documentation": artifact.documentation,
                "complexity_analysis": artifact.complexity_analysis,
                "security_notes": artifact.security_notes,
                "run_instructions": artifact.run_instructions,
            },
            "metadata": {
                "agent_version": tpca_core.version,
                "substrate": tpca_core.substrate,
                "mode": "autonomous",
                "language": code_request.language,
                "complexity_level": code_request.complexity,
            },
        }

        return jsonify(response), 200

    except Exception as e:
        logger.error(f"Error in generate_code: {str(e)}", exc_info=True)
        return jsonify({"status": "error", "message": str(e), "type": type(e).__name__}), 500


@app.route("/api/status", methods=["GET"])
def get_status() -> tuple:
    """
    Get TPCA agent status and capabilities.

    Response JSON:
    {
        "status": "operational",
        "agent": "Thalos Prime Coding Agent (TPCA)",
        "version": "8.0",
        "substrate": "SBI Wetware-Hybrid Neural Matrix",
        "capabilities": [...],
        "supported_languages": [...],
        "modes": [...]
    }
    """
    return (
        jsonify(
            {
                "status": "operational",
                "agent": "Thalos Prime Coding Agent (TPCA)",
                "version": tpca_core.version,
                "substrate": tpca_core.substrate,
                "architecture": "Autonomous Expert System",
                "dependencies": "Zero external dependencies",
                "capabilities": [
                    "First-principles code analysis",
                    "Production-ready code generation",
                    "Comprehensive test suite generation",
                    "Security and complexity analysis",
                    "Cross-language support",
                    "Self-validating output",
                ],
                "supported_languages": [
                    "Python",
                    "JavaScript",
                    "TypeScript",
                    "Java",
                    "C#",
                    "C++",
                    "C",
                    "Go",
                    "Rust",
                    "Swift",
                    "Kotlin",
                    "PHP",
                    "Ruby",
                    "SQL",
                    "HTML/CSS",
                    "Bash",
                    "PowerShell",
                ],
                "modes": [
                    "full (Full Application)",
                    "function (Function Generation)",
                    "class (Class/OOP)",
                    "api (API/Backend)",
                    "algorithm (Algorithms)",
                    "debug (Debug/Fix)",
                    "optimize (Optimization)",
                    "explain (Code Explanation)",
                ],
            }
        ),
        200,
    )


@app.route("/api/health", methods=["GET"])
def health_check() -> tuple:
    """Simple health check endpoint."""
    return jsonify({"status": "healthy", "agent": "TPCA", "version": tpca_core.version}), 200


@app.route("/")
def index() -> tuple:
    """Root endpoint - redirect to status."""
    return (
        jsonify(
            {
                "message": "Thalos Prime Coding Agent (TPCA) API Server",
                "version": tpca_core.version,
                "endpoints": {
                    "/api/generate": "POST - Generate code",
                    "/api/status": "GET - Agent status",
                    "/api/health": "GET - Health check",
                },
            }
        ),
        200,
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="TPCA API Server")
    parser.add_argument("--port", type=int, default=5000, help="Port to run on")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host to bind to")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")

    args = parser.parse_args()

    print(f"""
╔══════════════════════════════════════════════════════════════════════╗
║  ⚡ THALOS PRIME CODING AGENT (TPCA) - API SERVER                     ║
║  Version: {tpca_core.version}                                                       ║
║  Substrate: {tpca_core.substrate}                         ║
║  Architecture: Autonomous Expert System                               ║
╚══════════════════════════════════════════════════════════════════════╝

Starting server on http://{args.host}:{args.port}
Press CTRL+C to stop
    """)

    app.run(host=args.host, port=args.port, debug=args.debug)
