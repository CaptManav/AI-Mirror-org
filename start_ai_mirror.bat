@echo off
title AI Mirror Launcher

echo =====================================
echo        Starting AI Mirror...
echo =====================================

REM Automatically move to this script's directory
cd /d "%~dp0"

REM Activate virtual environment
call venv\Scripts\activate

REM Start FastAPI server
start "AI Mirror Server" cmd /k "cd /d %~dp0 && venv\Scripts\activate && uvicorn app.main:app --host 127.0.0.1 --port 8000"

REM Start Email Worker
start "AI Mirror Worker" cmd /k "cd /d %~dp0 && venv\Scripts\activate && python -m app.email_worker"

REM Wait 3 seconds
timeout /t 3 >nul

REM Open browser
start http://127.0.0.1:8000

pause