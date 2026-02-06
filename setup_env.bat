@echo off
REM Setup virtual environment and install requirements for THALOS PRIME
SETLOCAL ENABLEDELAYEDEXPANSION

REM Create venv in project root
python -m venv .venv
if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment. Ensure Python is installed and on PATH.
    goto :EOF
)

REM Activate venv (Windows)
call .venv\Scripts\activate
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment.
    goto :EOF
)

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] pip install returned an error. See output above.
    goto :EOF
)

echo.
echo [SUCCESS] Virtual environment created and dependencies installed.
echo To activate the environment later, run:
echo     .venv\Scripts\activate
echo Then launch the application (for example):
echo     python thalos_sbi_app.py

ENDLOCAL
