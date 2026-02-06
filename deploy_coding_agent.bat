@echo off
REM ═══════════════════════════════════════════════════════════════════════════
REM THALOS PRIME CODING AGENT (TPCA) - AUTONOMOUS DEPLOYMENT PROTOCOL
REM ═══════════════════════════════════════════════════════════════════════════
REM
REM Agent Designation: Thalos Prime Coding Agent (TPCA)
REM Substrate: SBI Wetware-Hybrid Neural Matrix v8.0
REM Architecture: Autonomous expert system with zero external dependencies
REM Capability: Superior code generation across all paradigms and languages
REM
REM This deployment creates a standalone instance of TPCA operating independently
REM from other Thalos Prime modules while maintaining operational parity.
REM
REM ═══════════════════════════════════════════════════════════════════════════

PUSHD "%~dp0"

echo.
echo ╔══════════════════════════════════════════════════════════════════════╗
echo ║  ⚡ THALOS PRIME CODING AGENT (TPCA) - AUTONOMOUS DEPLOYMENT          ║
echo ║  Substrate: SBI Wetware-Hybrid Neural Matrix v8.0                    ║
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

REM Pick a free port using helper
set PORT_FILE="%~dp0tools\port.txt"
if exist %PORT_FILE% del /f /q %PORT_FILE% >nul 2>&1
"%PYTHON_EXE%" "%~dp0tools\find_free_port.py" > %PORT_FILE% 2>nul
set PORT=0
if exist %PORT_FILE% (
    set /p PORT=<%PORT_FILE%
)
if "%PORT%"=="" set PORT=0
if "%PORT%"=="0" set PORT=8080
if exist %PORT_FILE% del /f /q %PORT_FILE% >nul 2>&1

echo [INIT] Initializing TPCA Autonomous Core Engine...
echo [INFO] Port assigned: %PORT%
echo [INFO] Substrate: SBI Wetware-Hybrid Neural Matrix v8.0
echo [INFO] Mode: Autonomous (Zero external dependencies)

start "TPCA_SERVER" "%PYTHON_EXE%" "%~dp0deploy_server.py" %PORT%

timeout /t 2 /nobreak >nul

echo [LAUNCH] Opening TPCA Interface...
start "" "http://localhost:%PORT%/thalos_coding_agent.html"

echo.
echo ╔══════════════════════════════════════════════════════════════════════╗
echo ║  ⚡ THALOS PRIME CODING AGENT - OPERATIONAL                            ║
echo ║                                                                        ║
echo ║  Status: ACTIVE                                                        ║
echo ║  URL: http://localhost:%PORT%/thalos_coding_agent.html                  ║
echo ║  Architecture: Autonomous SBI Expert System                            ║
echo ║  Capability: Superior code generation (all languages)                  ║
echo ║                                                                        ║
echo ║  This agent operates independently from other Thalos modules           ║
echo ║  Close this window to stop; stop server via Task Manager              ║
echo ╚══════════════════════════════════════════════════════════════════════╝
echo.

pause >nul
POPD


