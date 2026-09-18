@echo off
chcp 65001 >nul
cd /d %~dp0\backend
start "" "..\web-screen\index.html"
echo Starting API at http://127.0.0.1:8000/docs
.venv\Scripts\python.exe -m uvicorn app.main:app --reload
pause
