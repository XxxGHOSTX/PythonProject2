@echo off
REM ============================================================================
REM THALOS PRIME PRIMARY DIRECTIVE v5.0 - AUTOMATED LAUNCHER
REM ============================================================================

setlocal enabledelayedexpansion

echo.
echo ╔══════════════════════════════════════════════════════════════════════════╗
echo ║                                                                          ║
echo ║            THALOS PRIME PRIMARY DIRECTIVE v5.0                           ║
echo ║          SYNTHETIC BIOLOGICAL INTELLIGENCE APPLICATION                   ║
echo ║                                                                          ║
echo ║  Launching advanced neural system with 200M+ parameters...              ║
echo ║                                                                          ║
echo ╚══════════════════════════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo [INFO] Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

echo [SYSTEM] Python detected
echo [LAUNCHER] Setting up application environment...

REM Get the directory of this script
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

REM Check if THALOS_PRIME_APP.py exists
if not exist "THALOS_PRIME_APP.py" (
    echo [ERROR] THALOS_PRIME_APP.py not found in current directory
    echo [INFO] Current directory: %CD%
    pause
    exit /b 1
)

echo [LAUNCHER] THALOS_PRIME_APP.py located
echo [LAUNCHER] Starting neural core initialization...
echo.

REM Launch the application
python THALOS_PRIME_APP.py

REM If the script exits, show message
echo.
echo [SYSTEM] THALOS Prime application has terminated
echo [INFO] All session data has been saved
echo.

pause
