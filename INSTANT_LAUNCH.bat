@echo off
REM HYPER-NEXTUS INSTANT LAUNCH - Zero Configuration Required
SETLOCAL
PUSHD "%~dp0"
if exist ".venv\Scripts\python.exe" (
    start "HYPER-NEXTUS" .venv\Scripts\python.exe hyper_nextus_server.py
) else (
    python -m venv .venv
    .venv\Scripts\python.exe -m pip install -q -r requirements.txt
    start "HYPER-NEXTUS" .venv\Scripts\python.exe hyper_nextus_server.py
)
timeout /t 2 >nul
start http://127.0.0.1:5000/thalos_celestial.html
POPD
ENDLOCAL
