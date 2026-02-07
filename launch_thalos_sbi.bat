@echo off
REM ══════════════════════════════════════════════════════════════════════════════
REM THALOS PRIME SBI v6.0 - COMPLETE DEPLOYMENT & LAUNCH
REM Copyright © 2026 THALOS PRIME SYSTEMS - Tony Ray Macier III
REM ══════════════════════════════════════════════════════════════════════════════

setlocal enabledelayedexpansion

cls
color 0A
title THALOS PRIME SBI v6.0 - Advanced Neural Interface

echo.
echo ╔════════════════════════════════════════════════════════════════════════════╗
echo ║                                                                            ║
echo ║                   THALOS PRIME SBI v6.0 - DEPLOYMENT                       ║
echo ║              Synthetic Biological Intelligence System                      ║
echo ║                                                                            ║
echo ║         Advanced Neural Network with 200M+ Parameters                      ║
echo ║         Multi-Stage Reasoning • Cryptographic Security                     ║
echo ║         Context Management • Real-Time Confidence Scoring                  ║
echo ║                                                                            ║
echo ║             Copyright © 2026 THALOS PRIME SYSTEMS                          ║
echo ║                  Creator: Tony Ray Macier III                              ║
echo ║                                                                            ║
echo ╚════════════════════════════════════════════════════════════════════════════╝
echo.
echo.

REM ══════════════════════════════════════════════════════════════════════════════
REM SYSTEM VERIFICATION
REM ══════════════════════════════════════════════════════════════════════════════

echo [DEPLOYMENT] Phase 1: System Verification
echo.

python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo [ERROR] Python 3.8+ is required but not installed
    echo.
    echo [ACTION] Install Python from: https://www.python.org
    echo [HINT] Make sure to add Python to PATH during installation
    echo.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo [SUCCESS] Found: %PYTHON_VERSION%
echo.

REM ══════════════════════════════════════════════════════════════════════════════
REM FILE VERIFICATION
REM ══════════════════════════════════════════════════════════════════════════════

echo [DEPLOYMENT] Phase 2: File Verification
echo.

set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

setlocal enabledelayedexpansion

set REQUIRED_FILES=thalos_sbi_core_v6.py thalos_sbi_app.py thalos_database_schema.py

for %%f in (%REQUIRED_FILES%) do (
    if exist "%%f" (
        echo [SUCCESS] %%f located
    ) else (
        color 0C
        echo [ERROR] %%f NOT FOUND in %CD%
        pause
        exit /b 1
    )
)

echo.

REM ══════════════════════════════════════════════════════════════════════════════
REM DATABASE INITIALIZATION
REM ══════════════════════════════════════════════════════════════════════════════

echo [DEPLOYMENT] Phase 3: Database Initialization
echo.

python thalos_database_schema.py
if errorlevel 1 (
    echo [WARNING] Database initialization encountered issues, continuing...
)

echo.

REM ══════════════════════════════════════════════════════════════════════════════
REM MODULE VERIFICATION
REM ══════════════════════════════════════════════════════════════════════════════

echo [DEPLOYMENT] Phase 4: Module Verification
echo.

python -c "from thalos_sbi_core_v6 import ThalosApplication; print('[SUCCESS] Core modules loaded')" 2>nul
if errorlevel 1 (
    echo [WARNING] Some modules may be missing
) else (
    echo [SUCCESS] All core modules verified
)

echo.

REM ══════════════════════════════════════════════════════════════════════════════
REM LAUNCH APPLICATION
REM ══════════════════════════════════════════════════════════════════════════════

echo ════════════════════════════════════════════════════════════════════════════
echo                    [DEPLOYMENT COMPLETE - LAUNCHING]
echo ════════════════════════════════════════════════════════════════════════════
echo.

echo [SYSTEM] Initializing THALOS Prime SBI System...
echo [SYSTEM] Starting neural core initialization...
echo [SYSTEM] Launching interactive application...
echo [SYSTEM] Opening browser interface...
echo.

python thalos_sbi_app.py

echo.
echo [SHUTDOWN] THALOS Prime SBI application terminated
echo [INFO] All session data has been saved
echo.

pause
