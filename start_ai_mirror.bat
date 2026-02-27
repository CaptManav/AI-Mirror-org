@echo off
title AI Mirror Launcher

echo =====================================
echo        Starting AI Mirror...
echo =====================================

REM Go to project directory (IMPORTANT)
cd /d "C:\Users\MANAV\Desktop\AI Mirror v1"

REM Activate venv
call venv\Scripts\activate

REM Start FastAPI server in new window
start "AI Mirror Server" cmd /k "cd /d C:\Users\MANAV\Desktop\AI Mirror v1 && venv\Scripts\activate && uvicorn app.main:app --host 127.0.0.1 --port 8000"

REM Start Email Worker in new window
start "AI Mirror Worker" cmd /k "cd /d C:\Users\MANAV\Desktop\AI Mirror v1 && venv\Scripts\activate && python -m app.email_worker"

REM Wait 3 seconds
timeout /t 3 >nul

REM Open browser
start http://127.0.0.1:8000

pause