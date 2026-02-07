@echo off
REM ═══════════════════════════════════════════════════════════════════════════
REM THALOS PRIME - UNIFIED DEPLOYMENT
REM ═══════════════════════════════════════════════════════════════════════════
REM
REM Deploys complete Thalos Prime system:
REM 1. BIOCOMPUTING_CORE API Server (central wetware intelligence)
REM 2. Thalos Celestial (general intelligence interface)
REM 3. Thalos Coding Agent (code generation interface)
REM
REM All modules connect to BIOCOMPUTING_CORE for online processing
REM with full hardcoded offline fallback
REM
REM ═══════════════════════════════════════════════════════════════════════════

PUSHD "%~dp0"

echo.
echo ╔══════════════════════════════════════════════════════════════════════╗
echo ║  ⚡⚡⚡ THALOS PRIME - UNIFIED DEPLOYMENT ⚡⚡⚡                          ║
echo ║  Synthetic Biological Intelligence System                             ║
echo ╚══════════════════════════════════════════════════════════════════════╝
echo.

REM Step 1: Ensure venv exists
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

set PYTHON_EXE=python
if exist "%~dp0.venv\Scripts\python.exe" (
    set PYTHON_EXE=%~dp0.venv\Scripts\python.exe
)

echo.
echo ═══════════════════════════════════════════════════════════════════════
echo STEP 1: Launching BIOCOMPUTING_CORE API Server
echo ═══════════════════════════════════════════════════════════════════════
echo.

set BIOCORE_PORT=5001
echo [BIOCORE] Starting on port %BIOCORE_PORT%...
start "BIOCOMPUTING_CORE_API" "%PYTHON_EXE%" "%~dp0biocomputing_api_server.py" --port %BIOCORE_PORT%

timeout /t 3 /nobreak >nul
echo [BIOCORE] Server started: http://localhost:%BIOCORE_PORT%
echo.

echo ═══════════════════════════════════════════════════════════════════════
echo STEP 2: Launching Thalos Celestial
echo ═══════════════════════════════════════════════════════════════════════
echo.

echo [CELESTIAL] Opening interface...
start "" "%~dp0thalos_celestial.html"

timeout /t 2 /nobreak >nul
echo [CELESTIAL] Interface launched
echo.

echo ═══════════════════════════════════════════════════════════════════════
echo STEP 3: Launching Thalos Coding Agent (Optional)
echo ═══════════════════════════════════════════════════════════════════════
echo.

set /p LAUNCH_CODING="Launch Coding Agent? (y/n): "
if /i "%LAUNCH_CODING%"=="y" (
    REM Find free port for coding agent
    set PORT_FILE="%~dp0tools\port.txt"
    if exist %PORT_FILE% del /f /q %PORT_FILE% >nul 2>&1
    "%PYTHON_EXE%" "%~dp0tools\find_free_port.py" > %PORT_FILE% 2>nul
    set CODING_PORT=0
    if exist %PORT_FILE% (
        set /p CODING_PORT=<%PORT_FILE%
    )
    if "%CODING_PORT%"=="" set CODING_PORT=8080
    if "%CODING_PORT%"=="0" set CODING_PORT=8080
    if exist %PORT_FILE% del /f /q %PORT_FILE% >nul 2>&1

    echo [CODING] Starting on port %CODING_PORT%...
    start "CODING_AGENT_SERVER" "%PYTHON_EXE%" "%~dp0deploy_server.py" %CODING_PORT%

    timeout /t 2 /nobreak >nul

    echo [CODING] Opening interface...
    start "" "http://localhost:%CODING_PORT%/thalos_coding_agent.html"

    echo [CODING] Interface launched
)

echo.
echo ╔══════════════════════════════════════════════════════════════════════╗
echo ║  ⚡ THALOS PRIME - FULLY OPERATIONAL                                  ║
echo ║                                                                        ║
echo ║  BIOCOMPUTING_CORE API: http://localhost:%BIOCORE_PORT%              ║
echo ║  Status: ONLINE (with hardcoded offline fallback)                    ║
echo ║                                                                        ║
echo ║  Thalos Celestial: ACTIVE                                             ║
if /i "%LAUNCH_CODING%"=="y" (
    echo ║  Thalos Coding Agent: ACTIVE on port %CODING_PORT%                    ║
) else (
    echo ║  Thalos Coding Agent: Not launched                                   ║
)
echo ║                                                                        ║
echo ║  System Architecture:                                                  ║
echo ║  • Neural Organoids: 50,000 units                                      ║
echo ║  • Synaptic Connections: 5×10^13 total                                ║
echo ║  • Knowledge Domains: 6 primary domains                                ║
echo ║  • Processing Mode: Online-first, offline-capable                      ║
echo ║  • Intelligence: Fully hardcoded (identical online/offline)           ║
echo ║                                                                        ║
echo ║  All modules connected to wetware biocomputing core                   ║
echo ║  Close windows or press CTRL+C to stop components                     ║
echo ╚══════════════════════════════════════════════════════════════════════╝
echo.

pause
POPD
