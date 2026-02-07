@echo off
REM ============================================================================
REM THALOS PRIME PRIMARY DIRECTIVE v5.0 - MASTER LAUNCHER
REM ============================================================================
REM This is the main entry point for the entire THALOS Prime system
REM It handles all startup, verification, and execution tasks

setlocal enabledelayedexpansion

title THALOS PRIME PRIMARY DIRECTIVE v5.0
color 0A

cls

echo.
echo ╔══════════════════════════════════════════════════════════════════════════╗
echo ║                                                                          ║
echo ║            THALOS PRIME PRIMARY DIRECTIVE v5.0                           ║
echo ║          SYNTHETIC BIOLOGICAL INTELLIGENCE APPLICATION                   ║
echo ║                                                                          ║
echo ║              Advanced Neural Network with 200M+ Parameters               ║
echo ║                                                                          ║
echo ║           Authorizing Primary Directive Execution Protocol...            ║
echo ║                                                                          ║
echo ╚══════════════════════════════════════════════════════════════════════════╝
echo.
timeout /t 2 /nobreak >nul

REM ============================================================================
REM INITIALIZATION PHASE
REM ============================================================================

echo [MASTER LAUNCHER] Initializing startup sequence...
echo.

set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

REM Check Python
echo [SYSTEM CHECK] Verifying Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo [CRITICAL ERROR] Python is not installed or not in PATH
    echo.
    echo Please install Python 3.8+ from: https://www.python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo [SUCCESS] Found: %PYTHON_VERSION%
echo.

REM ============================================================================
REM STARTUP MENU
REM ============================================================================

echo [MENU] Select startup option:
echo.
echo   1. Launch THALOS Prime (Normal Mode)
echo   2. Run Setup Wizard
echo   3. Show Quick Reference
echo   4. Exit
echo.

set /p CHOICE="Enter choice (1-4): "

if "%CHOICE%"=="1" goto LAUNCH_APP
if "%CHOICE%"=="2" goto SETUP
if "%CHOICE%"=="3" goto QUICK_REF
if "%CHOICE%"=="4" goto EXIT_APP
goto MENU

:LAUNCH_APP
echo.
echo [LAUNCHER] Starting THALOS Prime Application...
echo [LAUNCHER] Initializing neural core...
echo [LAUNCHER] Loading interface components...
echo.

python THALOS_PRIME_APP.py
goto END

:SETUP
echo.
echo [SETUP WIZARD] Running system verification...
echo.

if exist setup_thalos.bat (
    call setup_thalos.bat
) else (
    echo [ERROR] setup_thalos.bat not found
    echo.
)

pause
goto MENU

:QUICK_REF
echo.
type QUICK_START_THALOS.txt
echo.
pause
goto MENU

:EXIT_APP
echo.
echo [SHUTDOWN] Thank you for using THALOS Prime Primary Directive v5.0
echo [SHUTDOWN] Session terminated cleanly
echo.
exit /b 0

:END
echo.
echo [SHUTDOWN] THALOS Prime Primary Directive has been deactivated
echo [SYSTEM] All sessions have been saved
echo.
pause
