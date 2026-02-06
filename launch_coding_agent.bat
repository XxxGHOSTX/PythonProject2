@echo off
REM ═══════════════════════════════════════════════════════════════════════════════
REM  THALOS PRIME CODING AGENT - Dedicated Launcher
REM  Superior SBI Code Generation Interface
REM ═══════════════════════════════════════════════════════════════════════════════

SETLOCAL ENABLEDELAYEDEXPANSION
PUSHD "%~dp0"

echo.
echo  ╔═══════════════════════════════════════════════════════════════════════╗
echo  ║           THALOS PRIME CODING AGENT - SUPERIOR SBI v8.0               ║
echo  ║                  Advanced Code Generation System                       ║
echo  ╚═══════════════════════════════════════════════════════════════════════╝
echo.

REM Create and activate venv if missing
IF NOT EXIST .venv (
    echo [SETUP] Creating virtual environment...
    python -m venv .venv
)

call .venv\Scripts\activate >nul 2>&1

REM Install requirements if needed
python -m pip install -r requirements.txt -q >nul 2>&1

REM Determine python executable
set PYTHON_EXE=python
if exist "%~dp0.venv\Scripts\python.exe" (
    set PYTHON_EXE=%~dp0.venv\Scripts\python.exe
)

REM Find a free port
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

echo [INFO] Starting Coding Agent server on port %PORT%...
echo.

REM Start the server in a new minimized window
start /min "THALOS_CODING_AGENT_SERVER" "%PYTHON_EXE%" -c "import http.server, socketserver, os; os.chdir(r'%~dp0'); httpd = socketserver.TCPServer(('', %PORT%), http.server.SimpleHTTPRequestHandler); print('Server running...'); httpd.serve_forever()"

REM Wait for server to start
timeout /t 2 /nobreak >nul

REM Open the Coding Agent interface
echo [LAUNCH] Opening Coding Agent in browser...
start "" "http://localhost:%PORT%/thalos_coding_agent.html"

echo.
echo  ╔═══════════════════════════════════════════════════════════════════════╗
echo  ║  ⚡ THALOS PRIME CODING AGENT is now running!                          ║
echo  ║                                                                        ║
echo  ║  URL: http://localhost:%PORT%/thalos_coding_agent.html                   ║
echo  ║                                                                        ║
echo  ║  The server is running in a minimized window.                          ║
echo  ║  Close this window or press any key to continue...                     ║
echo  ╚═══════════════════════════════════════════════════════════════════════╝
echo.

pause >nul

POPD
ENDLOCAL
