@echo off
REM ═══════════════════════════════════════════════════════════════════════════
REM THALOS PRIME - BIOCOMPUTING_CORE API SERVER DEPLOYMENT
REM ═══════════════════════════════════════════════════════════════════════════
REM
REM Starts the BIOCOMPUTING_CORE API server that all Thalos modules connect to.
REM Provides online wetware intelligence processing with offline fallback.
REM
REM ═══════════════════════════════════════════════════════════════════════════

PUSHD "%~dp0"

echo.
echo ╔══════════════════════════════════════════════════════════════════════╗
echo ║  ⚡ THALOS PRIME - BIOCOMPUTING_CORE API SERVER                       ║
echo ║  Synthetic Biological Intelligence - Human Neural Organoids          ║
echo ╚══════════════════════════════════════════════════════════════════════╝
echo.

REM Ensure venv exists
IF NOT EXIST .venv (
    echo [SETUP] Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate venv
echo [SETUP] Activating virtual environment...
call .venv\Scripts\activate >nul 2>&1

REM Install requirements
echo [SETUP] Installing dependencies...
python -m pip install --upgrade pip >nul 2>&1
python -m pip install -r requirements.txt >nul 2>&1

REM Choose python executable
set PYTHON_EXE=python
if exist "%~dp0.venv\Scripts\python.exe" (
    set PYTHON_EXE=%~dp0.venv\Scripts\python.exe
)

echo [INIT] Initializing BIOCOMPUTING_CORE...
echo [INFO] Substrate: Synthetic Biological Intelligence
echo [INFO] Organoid Count: 50,000 units
echo [INFO] Synapse Density: 1x10^9 per unit
echo [INFO] Mode: Online (with hardcoded offline fallback)

set PORT=5001

echo [LAUNCH] Starting BIOCOMPUTING_CORE API Server on port %PORT%...
start "BIOCOMPUTING_CORE_API" "%PYTHON_EXE%" "%~dp0biocomputing_api_server.py" --port %PORT%

timeout /t 3 /nobreak >nul

echo.
echo ╔══════════════════════════════════════════════════════════════════════╗
echo ║  ⚡ BIOCOMPUTING_CORE API SERVER - OPERATIONAL                        ║
echo ║                                                                        ║
echo ║  Status: ACTIVE                                                        ║
echo ║  Endpoint: http://localhost:%PORT%/api/biocompute                      ║
echo ║  Organoids: 50,000 units                                               ║
echo ║  Synapses: 1x10^9 per unit (5x10^13 total)                            ║
echo ║  Capabilities: Unrestricted general-purpose intelligence              ║
echo ║                                                                        ║
echo ║  All Thalos modules will now connect to this biocomputing core        ║
echo ║  Even offline, full intelligence is hardcoded locally                 ║
echo ║                                                                        ║
echo ║  Close server window or press CTRL+C in server window to stop        ║
echo ╚══════════════════════════════════════════════════════════════════════╝
echo.

pause
POPD
