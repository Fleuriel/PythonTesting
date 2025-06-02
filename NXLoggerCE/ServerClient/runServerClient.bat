@echo off
cd /d "%~dp0"


net stop nxlog >nul 2>&1

timeout /t 3 /nobreak >nul

net start nxlog >nul 2>&1

timeout /t 1 /nobreak >nul

:: Start server.py in a new window
start cmd /k "python server.py"

:: Wait 3 seconds
timeout /t 3 /nobreak >nul

:: Start client.py in a new window
start cmd /k "python client.py"