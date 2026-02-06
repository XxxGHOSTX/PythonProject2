@echo off
REM Automated deployment: set up venv, install requirements, run the deployment server

PUSHD "%~dp0"

REM Create and activate venv if missing
IF NOT EXIST .venv (
    echo [.venv] Creating virtual environment...
    python -m venv .venv
)

call .venv\Scripts\activate

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo [ERROR] Deployment setup failed during pip install.
    POPD
    goto :EOF
)

REM Determine python executable (prefer venv)
set PYTHON_EXE=python
if exist "%~dp0.venv\Scripts\python.exe" (
    set PYTHON_EXE=%~dp0.venv\Scripts\python.exe
)

REM Use helper script to pick a free port (write to temp file then read it)
set PORT_FILE="%~dp0tools\port.txt"
if exist %PORT_FILE% del /f /q %PORT_FILE% >nul 2>&1
"%PYTHON_EXE%" "%~dp0tools\find_free_port.py" > %PORT_FILE% 2>nul || (
    echo [WARN] find_free_port helper failed
)

set PORT=0
if exist %PORT_FILE% (
    set /p PORT=<%PORT_FILE%
)

if "%PORT%"=="" set PORT=0
if "%PORT%"=="0" (
    echo [WARN] find_free_port returned 0 or failed; defaulting to 8080
    set PORT=8080
)

REM Clean up temp file
if exist %PORT_FILE% del /f /q %PORT_FILE% >nul 2>&1

echo [INFO] Selected port %PORT% to start the server.
if exist "%~dp0.venv\Scripts\python.exe" (
    echo [INFO] Launching deployment server in a new window using venv python on port %PORT%...
    start "THALOS_DEPLOY_SERVER" "%~dp0.venv\Scripts\python.exe" "%~dp0deploy_server.py" %PORT%
) else (
    echo [INFO] venv python not found; launching with system python in a new window on port %PORT%...
    start "THALOS_DEPLOY_SERVER" python "%~dp0deploy_server.py" %PORT%
)

echo [INFO] Server started (check the new window) or visit http://localhost:%PORT%

POPD
