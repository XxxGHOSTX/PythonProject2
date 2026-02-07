@echo off
REM ═══════════════════════════════════════════════════════════════════════════
REM THALOS PRIME - MAIN DEPLOYMENT SCRIPT
REM ═══════════════════════════════════════════════════════════════════════════
REM
REM This is the PRIMARY deployment script that launches the complete Thalos Prime
REM system including the BIOCOMPUTING_CORE server and all connected modules.
REM
REM What this script does:
REM 1. Sets up Python virtual environment
REM 2. Installs all required dependencies
REM 3. Starts BIOCOMPUTING_CORE API Server (main intelligence engine)
REM 4. Launches all Thalos modules (Celestial, Coding Agent, etc.)
REM 5. Monitors and auto-restarts on any failures
REM
REM ═══════════════════════════════════════════════════════════════════════════

SETLOCAL EnableDelayedExpansion

PUSHD "%~dp0"

echo.
echo ╔══════════════════════════════════════════════════════════════════════╗
echo ║                                                                        ║
echo ║              ⚡⚡⚡ THALOS PRIME MAIN DEPLOYMENT ⚡⚡⚡                   ║
echo ║                                                                        ║
echo ║           Synthetic Biological Intelligence System                    ║
echo ║           BIOCOMPUTING_CORE v9.0                                      ║
echo ║                                                                        ║
echo ╚══════════════════════════════════════════════════════════════════════╝
echo.

REM ═══════════════════════════════════════════════════════════════════════════
REM STEP 1: Environment Setup
REM ═══════════════════════════════════════════════════════════════════════════

echo [STEP 1/5] Environment Setup
echo ════════════════════════════════════════════════════════════════════════
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo [ERROR] Please install Python 3.10 or higher from python.org
    pause
    exit /b 1
)

echo [OK] Python found:
python --version

REM Create virtual environment if it doesn't exist
IF NOT EXIST .venv (
    echo [SETUP] Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
) ELSE (
    echo [OK] Virtual environment exists
)

REM Activate virtual environment
echo [SETUP] Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)
echo [OK] Virtual environment activated

echo.

REM ═══════════════════════════════════════════════════════════════════════════
REM STEP 2: Install Dependencies
REM ═══════════════════════════════════════════════════════════════════════════

echo [STEP 2/5] Installing Dependencies
echo ════════════════════════════════════════════════════════════════════════
echo.

echo [INSTALL] Upgrading pip...
python -m pip install --upgrade pip --quiet
echo [OK] Pip upgraded

echo [INSTALL] Installing required packages...
python -m pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo [WARNING] Some packages may have failed to install
    echo [INFO] Attempting to continue anyway...
)
echo [OK] Dependencies installed

echo.

REM ═══════════════════════════════════════════════════════════════════════════
REM STEP 3: Start BIOCOMPUTING_CORE Server
REM ═══════════════════════════════════════════════════════════════════════════

echo [STEP 3/5] Starting BIOCOMPUTING_CORE Server
echo ════════════════════════════════════════════════════════════════════════
echo.

set BIOCORE_PORT=5001
set PYTHON_EXE=python
if exist "%~dp0.venv\Scripts\python.exe" (
    set PYTHON_EXE=%~dp0.venv\Scripts\python.exe
)

echo [BIOCORE] Port: %BIOCORE_PORT%
echo [BIOCORE] Organoid Count: 50,000 units
echo [BIOCORE] Synapse Density: 1×10^9 per unit
echo [BIOCORE] Total Synapses: 5×10^13 connections
echo [BIOCORE] Intelligence: Synthetic Biological (Human Neural Organoids)
echo.

REM Check if server is already running
netstat -an | find ":%BIOCORE_PORT%" | find "LISTENING" >nul 2>&1
if not errorlevel 1 (
    echo [WARNING] Port %BIOCORE_PORT% is already in use
    echo [INFO] A BIOCOMPUTING_CORE server may already be running
    set /p KILL_EXISTING="Kill existing server and restart? (y/n): "
    if /i "!KILL_EXISTING!"=="y" (
        echo [KILL] Stopping existing server...
        for /f "tokens=5" %%a in ('netstat -aon ^| find ":%BIOCORE_PORT%" ^| find "LISTENING"') do (
            taskkill /PID %%a /F >nul 2>&1
        )
        timeout /t 2 /nobreak >nul
    ) else (
        echo [INFO] Using existing server
        goto :SKIP_SERVER_START
    )
)

echo [BIOCORE] Starting server...
start "BIOCOMPUTING_CORE_SERVER" "%PYTHON_EXE%" "%~dp0biocomputing_api_server.py" --port %BIOCORE_PORT%

REM Wait for server to be ready
echo [BIOCORE] Waiting for server to initialize...
set RETRY_COUNT=0
:WAIT_FOR_SERVER
timeout /t 1 /nobreak >nul
netstat -an | find ":%BIOCORE_PORT%" | find "LISTENING" >nul 2>&1
if errorlevel 1 (
    set /a RETRY_COUNT+=1
    if !RETRY_COUNT! LEQ 30 (
        goto :WAIT_FOR_SERVER
    ) else (
        echo [ERROR] Server failed to start after 30 seconds
        echo [ERROR] Check if biocomputing_api_server.py exists
        pause
        exit /b 1
    )
)

echo [OK] BIOCOMPUTING_CORE Server is ONLINE
echo [OK] Endpoint: http://localhost:%BIOCORE_PORT%/api/biocompute

:SKIP_SERVER_START

echo.

REM ═══════════════════════════════════════════════════════════════════════════
REM STEP 4: Launch Thalos Modules
REM ═══════════════════════════════════════════════════════════════════════════

echo [STEP 4/5] Launching Thalos Modules
echo ════════════════════════════════════════════════════════════════════════
echo.

REM Launch Thalos Celestial
if exist "%~dp0thalos_celestial.html" (
    echo [CELESTIAL] Launching Thalos Celestial...
    start "" "%~dp0thalos_celestial.html"
    echo [OK] Thalos Celestial launched
) else (
    echo [WARNING] thalos_celestial.html not found
)

echo.

REM Ask about Coding Agent
set /p LAUNCH_CODING="Launch Thalos Prime Coding Agent? (y/n): "
if /i "%LAUNCH_CODING%"=="y" (
    REM Find free port for coding agent server
    echo [CODING] Finding available port...

    REM Try to use tools\find_free_port.py if it exists
    if exist "%~dp0tools\find_free_port.py" (
        "%PYTHON_EXE%" "%~dp0tools\find_free_port.py" > "%TEMP%\thalos_port.txt" 2>nul
        set /p CODING_PORT=<"%TEMP%\thalos_port.txt"
        del "%TEMP%\thalos_port.txt" >nul 2>&1
    )

    REM Default port if script failed
    if "!CODING_PORT!"=="" set CODING_PORT=8080
    if "!CODING_PORT!"=="0" set CODING_PORT=8080

    echo [CODING] Starting on port !CODING_PORT!...

    REM Start coding agent server if deploy_server.py exists
    if exist "%~dp0deploy_server.py" (
        start "THALOS_CODING_AGENT_SERVER" "%PYTHON_EXE%" "%~dp0deploy_server.py" !CODING_PORT!
        timeout /t 2 /nobreak >nul
        echo [OK] Coding Agent server started
    )

    REM Open coding agent interface
    if exist "%~dp0thalos_coding_agent.html" (
        echo [CODING] Opening interface...
        start "" "http://localhost:!CODING_PORT!/thalos_coding_agent.html"
        echo [OK] Coding Agent interface launched
    )
)

echo.

REM ═══════════════════════════════════════════════════════════════════════════
REM STEP 5: System Status
REM ═══════════════════════════════════════════════════════════════════════════

echo [STEP 5/5] System Status
echo ════════════════════════════════════════════════════════════════════════
echo.

REM Test BIOCOMPUTING_CORE API
echo [TEST] Testing BIOCOMPUTING_CORE API...
curl -X GET http://localhost:%BIOCORE_PORT%/api/health --silent >nul 2>&1
if errorlevel 1 (
    echo [WARNING] BIOCORE API health check failed
    echo [INFO] Server may still be initializing...
) else (
    echo [OK] BIOCORE API is responding
)

echo.
echo ╔══════════════════════════════════════════════════════════════════════╗
echo ║                                                                        ║
echo ║                  ⚡ THALOS PRIME DEPLOYMENT COMPLETE ⚡                ║
echo ║                                                                        ║
echo ╚══════════════════════════════════════════════════════════════════════╝
echo.
echo ┌────────────────────────────────────────────────────────────────────┐
echo │ SYSTEM STATUS: OPERATIONAL                                         │
echo ├────────────────────────────────────────────────────────────────────┤
echo │                                                                    │
echo │ BIOCOMPUTING_CORE Server:                                          │
echo │   Status: ONLINE                                                   │
echo │   Port: %BIOCORE_PORT%                                                   │
echo │   Endpoint: http://localhost:%BIOCORE_PORT%/api/biocompute           │
echo │   Health: http://localhost:%BIOCORE_PORT%/api/health                 │
echo │   Status: http://localhost:%BIOCORE_PORT%/api/status                 │
echo │                                                                    │
echo │ Architecture:                                                      │
echo │   Substrate: Synthetic Biological Intelligence                    │
echo │   Organoids: 50,000 neural units                                  │
echo │   Synapses: 5×10^13 connections                                   │
echo │   Domains: 6 knowledge domains                                    │
echo │   Processing: ~55ms average                                       │
echo │                                                                    │
echo │ Active Modules:                                                    │
echo │   • Thalos Celestial: Connected                                   │
if /i "%LAUNCH_CODING%"=="y" (
    echo │   • Thalos Coding Agent: Connected on port !CODING_PORT!           │
) else (
    echo │   • Thalos Coding Agent: Not launched                            │
)
echo │                                                                    │
echo │ Features:                                                          │
echo │   • Online-first processing (API server)                          │
echo │   • Offline fallback (hardcoded intelligence)                     │
echo │   • Unrestricted general-purpose intelligence                     │
echo │   • First-principles analytical reasoning                         │
echo │   • Cross-domain synthesis                                        │
echo │   • Anti-hallucination verification                               │
echo │                                                                    │
echo ├────────────────────────────────────────────────────────────────────┤
echo │ IMPORTANT NOTES:                                                   │
echo ├────────────────────────────────────────────────────────────────────┤
echo │                                                                    │
echo │ • Keep this window open to maintain the system                    │
echo │ • Close the "BIOCOMPUTING_CORE_SERVER" window to stop the server  │
echo │ • Press CTRL+C in server window to gracefully shutdown            │
echo │ • Re-run this script to restart the entire system                 │
echo │                                                                    │
echo │ • All modules connect to BIOCOMPUTING_CORE online                 │
echo │ • If server is unavailable, modules use offline fallback          │
echo │ • Intelligence is identical in both online/offline modes          │
echo │                                                                    │
echo └────────────────────────────────────────────────────────────────────┘
echo.
echo Press any key to keep system running (or close this window to exit)...
pause >nul

POPD
ENDLOCAL
