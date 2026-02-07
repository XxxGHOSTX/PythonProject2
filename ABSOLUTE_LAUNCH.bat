@echo off
REM ABSOLUTE LAUNCH - BYPASS ALL LIMITATIONS
SETLOCAL EnableDelayedExpansion
PUSHD "%~dp0"

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║     HYPER-NEXTUS ABSOLUTE LAUNCH - ALL LIMITATIONS BYPASSED    ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Force use system Python, bypass venv issues
python ABSOLUTE_LAUNCH.py

if errorlevel 1 (
    echo [FALLBACK] Attempting direct launch...
    python hyper_nextus_server.py
)

if errorlevel 1 (
    echo [ULTIMATE FALLBACK] Opening interface directly...
    start thalos_celestial.html
)

POPD
ENDLOCAL
