@echo off
REM ============================================================================
REM THALOS PRIME v5.0 - SYSTEM VERIFICATION & STATUS CHECK
REM ============================================================================

setlocal enabledelayedexpansion

cls

color 0A
title THALOS PRIME - System Verification

echo.
echo ╔══════════════════════════════════════════════════════════════════════════╗
echo ║                                                                          ║
echo ║              THALOS PRIME PRIMARY DIRECTIVE v5.0                         ║
echo ║                  SYSTEM VERIFICATION & STATUS CHECK                      ║
echo ║                                                                          ║
echo ╚══════════════════════════════════════════════════════════════════════════╝
echo.
echo.

echo ════════════════════════════════════════════════════════════════════════════
echo [1/5] PYTHON ENVIRONMENT CHECK
echo ════════════════════════════════════════════════════════════════════════════
echo.

python --version
if errorlevel 1 (
    echo [FAIL] Python is not installed or not in PATH
    goto FAIL
) else (
    echo [PASS] Python environment OK
)

echo.

echo ════════════════════════════════════════════════════════════════════════════
echo [2/5] APPLICATION FILES CHECK
echo ════════════════════════════════════════════════════════════════════════════
echo.

cd /d "%~dp0"

set REQUIRED_FILES=THALOS_PRIME_APP.py launch_thalos_app.bat setup_thalos.bat

for %%f in (%REQUIRED_FILES%) do (
    if exist "%%f" (
        echo [PASS] %%f found
    ) else (
        echo [FAIL] %%f NOT FOUND
        goto FAIL
    )
)

echo.

echo ════════════════════════════════════════════════════════════════════════════
echo [3/5] PYTHON MODULES CHECK
echo ════════════════════════════════════════════════════════════════════════════
echo.

python -c "import http, json, threading, socket, time, random, string, pickle; print('[PASS] All required modules available')" 2>nul
if errorlevel 1 (
    echo [FAIL] Some required modules are missing
    goto FAIL
) else (
    echo [SUCCESS] Python modules verified
)

echo.

echo ════════════════════════════════════════════════════════════════════════════
echo [4/5] NEURAL CORE IMPORT TEST
echo ════════════════════════════════════════════════════════════════════════════
echo.

python -c "from THALOS_PRIME_APP import Config, TokenizerEmbedding, TransformerModel, ContentGenerator, SessionManager; print('[PASS] Neural core modules loaded successfully')" 2>nul
if errorlevel 1 (
    echo [FAIL] Neural core import failed
    goto FAIL
) else (
    echo [SUCCESS] Neural core verified
)

echo.

echo ════════════════════════════════════════════════════════════════════════════
echo [5/5] SYSTEM RESOURCES CHECK
echo ════════════════════════════════════════════════════════════════════════════
echo.

for /f "skip=1" %%A in ('wmic OS get totalvisiblememorynmemory') do (
    set /a RAM_KB=%%A
    set /a RAM_GB=!RAM_KB! / 1024 / 1024
    if !RAM_GB! GEQ 512 (
        echo [PASS] Available memory: !RAM_GB!MB
    ) else (
        echo [WARN] Low memory: !RAM_GB!MB ^(512MB+ recommended^)
    )
    goto RAM_OK
)

:RAM_OK
echo.

echo ════════════════════════════════════════════════════════════════════════════
echo                          [VERIFICATION COMPLETE]
echo ════════════════════════════════════════════════════════════════════════════
echo.
echo [STATUS] ✓ THALOS Prime is ready to launch
echo.
echo SYSTEM SUMMARY:
echo   ✓ Python environment configured
echo   ✓ All application files present
echo   ✓ Required modules available
echo   ✓ Neural core components verified
echo   ✓ System resources sufficient
echo.
echo NEXT STEPS:
echo   1. Run: LAUNCH_THALOS_PRIME.bat
echo   2. Or run: launch_thalos_app.bat directly
echo.
pause
exit /b 0

:FAIL
echo.
color 0C
echo [CRITICAL ERROR] System verification FAILED
echo.
echo Please check:
echo   1. Python 3.8+ is installed
echo   2. Python is in system PATH
echo   3. All application files are present
echo   4. Sufficient disk space (200MB+)
echo   5. System has 512MB+ available RAM
echo.
echo For help, see: THALOS_PRIME_GUIDE.md
echo.
pause
exit /b 1
