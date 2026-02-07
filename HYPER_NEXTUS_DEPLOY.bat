@echo off
REM HYPER-NEXTUS RAPID DEPLOYMENT
REM Auto-setup, auto-configure, production-ready

SETLOCAL EnableDelayedExpansion
PUSHD "%~dp0"

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║     HYPER-NEXTUS UNIFIED DEPLOYMENT SYSTEM                     ║
echo ║     THALOS PRIME Ecosystem - Full Integration                  ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found - install Python 3.10+
    pause
    exit /b 1
)

REM Setup venv if needed
IF NOT EXIST .venv (
    echo [SETUP] Creating virtual environment...
    python -m venv .venv
)

REM Activate
call .venv\Scripts\activate.bat >nul 2>&1

REM Install deps
echo [INSTALL] Installing dependencies...
pip install -q --upgrade pip
pip install -q -r requirements.txt

REM Launch
echo [LAUNCH] Starting HYPER-NEXTUS server...
echo.
python hyper_nextus_server.py %*

POPD
ENDLOCAL
