@echo off
chcp 65001 >nul
cd /d %~dp0
echo [1/3] Creating venv...
python -m venv backend\.venv
echo [2/3] Installing core deps...
backend\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
echo [3/3] Importing sample data...
backend\.venv\Scripts\python.exe backend\app\ingestion\load.py
echo.
echo DONE. Now double-click run.bat to start.
pause
