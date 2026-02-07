@echo off
REM HYPER-NEXTUS AUTONOMOUS LAUNCHER
REM Self-healing, self-monitoring, zero manual intervention

SETLOCAL
PUSHD "%~dp0"

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║   HYPER-NEXTUS AUTONOMOUS MODE - ZERO INTERVENTION REQUIRED    ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Start autonomous core in background
start "HYPER-NEXTUS Autonomous Core" /MIN python autonomous_core.py

REM Wait briefly
timeout /t 2 /nobreak >nul

REM Open browser
start http://127.0.0.1:5000/thalos_celestial.html

echo.
echo ✓ Autonomous core running
echo ✓ System self-monitoring active
echo ✓ Auto-fix enabled
echo ✓ Browser launched
echo.
echo System will automatically:
echo   • Fix environment issues
echo   • Install missing packages
echo   • Restart server if needed
echo   • Resolve import errors
echo   • Maintain continuous operation
echo.
echo Close this window anytime - autonomous core continues running
echo.

POPD
ENDLOCAL
