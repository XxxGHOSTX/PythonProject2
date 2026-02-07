@echo off
REM Create desktop shortcut for Thalos Prime Coding Agent

set SCRIPT_DIR=%~dp0
set SHORTCUT_NAME=⚡ Thalos Coding Agent.lnk
set TARGET=%SCRIPT_DIR%deploy_coding_agent.bat
set DESKTOP=%USERPROFILE%\Desktop

powershell "$s=(New-Object -COM WScript.Shell).CreateShortcut('%DESKTOP%\%SHORTCUT_NAME%');$s.TargetPath='%TARGET%';$s.WorkingDirectory='%SCRIPT_DIR%';$s.Description='Thalos Prime Coding Agent - Autonomous SBI Expert System';$s.Save()"

echo Desktop shortcut created: %SHORTCUT_NAME%
pause
