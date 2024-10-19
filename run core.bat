@echo off
:: Prompt for administrator privileges
:: Get the current directory
set "scriptPath=%~dp0"

:: Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Requesting administrator access...
    powershell -Command "Start-Process cmd -ArgumentList '/c \"%~f0\"' -Verb runAs"
    exit /b
)

:: Run the Python script as administrator
cd /d "%scriptPath%"
python core.py

pause
