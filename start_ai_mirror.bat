@echo off
title AI Mirror Launcher

echo =====================================
echo        Starting AI Mirror...
echo =====================================

REM Go to project directory
cd /d "C:\Users\MANAV\Desktop\AI Mirror v1"

REM Activate virtual environment
call venv\Scripts\activate

echo Starting FastAPI Server...
start "AI Mirror Server" cmd /k ^
"cd /d C:\Users\MANAV\Desktop\AI Mirror v1 && ^
venv\Scripts\activate && ^
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

echo Starting Worker...
start "AI Mirror Worker" cmd /k ^
"cd /d C:\Users\MANAV\Desktop\AI Mirror v1 && ^
venv\Scripts\activate && ^
python -m app.email_worker"

REM Wait a bit for server to start
timeout /t 4 >nul

echo Opening Dashboard...
start http://127.0.0.1:8000

echo =====================================
echo        AI Mirror is running!
echo =====================================

pause