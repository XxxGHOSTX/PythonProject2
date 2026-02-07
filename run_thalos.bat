@echo off
REM Activate the project's virtual environment and run the desired Thalos app
REM Usage: run_thalos.bat [app]
REM Apps: sbi (default), prime, server, coding

SET APP=%1
IF "%APP%"=="" SET APP=sbi

REM Ensure running from project root
PUSHD "%~dp0"

REM Activate venv
IF EXIST .venv\Scripts\activate (
    call .venv\Scripts\activate
) ELSE (
    echo [WARNING] Virtual environment not found. Creating one now...
    python -m venv .venv
    call .venv\Scripts\activate
    python -m pip install --upgrade pip
    pip install -r requirements.txt
)

REM Launch selected app
IF /I "%APP%"=="sbi" (
    echo Launching thalos_sbi_app.py
    python thalos_sbi_app.py
) ELSE IF /I "%APP%"=="prime" (
    echo Launching THALOS_PRIME_APP.py
    python THALOS_PRIME_APP.py
) ELSE IF /I "%APP%"=="server" (
    echo Launching deploy_server.py
    python deploy_server.py
) ELSE IF /I "%APP%"=="coding" (
    echo Launching Thalos Prime Coding Agent...
    call "%~dp0launch_coding_agent.bat"
) ELSE (
    echo Unknown app '%APP%'. Valid options: sbi, prime, server, coding
)

POPD
