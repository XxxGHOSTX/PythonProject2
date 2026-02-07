@echo off
cls
echo ============================================================
echo           THALOS PRIME - VERSION SELECTOR
echo ============================================================
echo.
echo Select which version to launch:
echo.
echo [1] Thalos Prime v3.0 - Terminal Edition (Green Matrix)
echo [2] Thalos Prime v2.1 - Celestial Navigator (Amber/Gold)
echo.
echo [Q] Quit
echo.
echo ============================================================
echo.

choice /C 12Q /N /M "Enter your choice (1, 2, or Q): "

if errorlevel 3 goto :EOF
if errorlevel 2 goto celestial
if errorlevel 1 goto terminal

:terminal
echo.
echo Launching Terminal Edition...
start "" "%~dp0thalos_prime.html"
goto end

:celestial
echo.
echo Launching Celestial Navigator...
start "" "%~dp0thalos_celestial.html"
goto end

:end
echo.
echo ✓ Interface opened!
echo.
timeout /t 3
