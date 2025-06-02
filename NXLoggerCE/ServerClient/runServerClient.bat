@echo off
cd /d "%~dp0"

:: Start server.py in a new window
start cmd /k "python server.py"

:: Wait 3 seconds
timeout /t 3 /nobreak >nul

:: Start client.py in a new window
start cmd /k "python client.py"