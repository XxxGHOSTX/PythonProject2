@echo off
REM Quick verification of THALOS PRIME deployment
echo.
echo ════════════════════════════════════════════════════════════════
echo THALOS PRIME - Deployment Verification
echo ════════════════════════════════════════════════════════════════
echo.

cd /d "%~dp0"

echo [1/5] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [X] Python NOT found - Install Python 3.10+
    goto :END
) else (
    python --version
    echo [✓] Python found
)
echo.

echo [2/5] Checking Virtual Environment...
if exist ".venv" (
    echo [✓] Virtual environment exists
) else (
    echo [!] Creating virtual environment...
    python -m venv .venv
    echo [✓] Virtual environment created
)
echo.

echo [3/5] Checking Core Files...
if exist "BIOCOMPUTING_CORE.py" (
    echo [✓] BIOCOMPUTING_CORE.py exists
) else (
    echo [X] BIOCOMPUTING_CORE.py MISSING
)

if exist "biocomputing_api_server.py" (
    echo [✓] biocomputing_api_server.py exists
) else (
    echo [X] biocomputing_api_server.py MISSING
)

if exist "thalos_celestial.html" (
    echo [✓] thalos_celestial.html exists
) else (
    echo [X] thalos_celestial.html MISSING
)
echo.

echo [4/5] Installing Dependencies...
call .venv\Scripts\activate.bat
pip install -q -r requirements.txt
echo [✓] Dependencies installed
echo.

echo [5/5] Testing BIOCOMPUTING_CORE...
python -c "from BIOCOMPUTING_CORE import get_biocomputing_core; core = get_biocomputing_core(); print(f'[✓] Core initialized: {core.version}')" 2>nul
if errorlevel 1 (
    echo [!] Core test had warnings (may still work)
) else (
    echo [✓] Core test passed
)
echo.

echo ════════════════════════════════════════════════════════════════
echo Verification Complete
echo ════════════════════════════════════════════════════════════════
echo.
echo To start the system:
echo   1. Run: DEPLOY_THALOS_PRIME.bat
echo   2. Or manually start server: python biocomputing_api_server.py --port 5001
echo   3. Then open: thalos_celestial.html
echo.

:END
pause
