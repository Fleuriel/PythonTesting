@echo off
:: Check for administrator privileges
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Requesting administrator privileges...
    powershell -Command "Start-Process '%~f0' -Verb runAs"
    exit /b
)

:: If we're here, we are running as administrator
cd /d "%~dp0"

echo Restarting NXLog...
net stop nxlog >nul 2>&1
timeout /t 3 /nobreak >nul
net start nxlog >nul 2>&1
timeout /t 1 /nobreak >nul

:: Start server
start cmd /k "python server.py"

:: Delay and start client
timeout /t 3 /nobreak >nul
start cmd /k "python client.py"
