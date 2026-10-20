@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
cd /d "%~dp0"
set PYTHONPATH=%~dp0;%PYTHONPATH%

title SkillMatch IT - AI Job Matcher Launcher

echo ===================================================
echo           SkillMatch IT - Startup System
echo ===================================================
echo.

REM 1. Check Python
where python >nul 2>&1
if errorlevel 1 (
    where py >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] Python not found. Please install Python 3.8+ and add it to PATH.
        pause
        exit /b 1
    ) else (
        set PYCMD=py
    )
) else (
    set PYCMD=python
)

for /f "tokens=*" %%v in ('!PYCMD! --version 2^>^&1') do set PYVER=%%v
echo [OK] Found !PYVER!
echo.

REM 2. Fast Dependency Check (Only run pip if an import is missing)
echo [1/3] Checking dependencies...
!PYCMD! -c "import fastapi, uvicorn, pandas, sklearn, numpy, pydantic, joblib, requests" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing or updating dependencies from requirements.txt...
    !PYCMD! -m pip install -r requirements.txt --disable-pip-version-check
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies. Please check your internet connection.
        pause
        exit /b 1
    )
    echo [OK] Dependencies installed successfully.
) else (
    echo [OK] All dependencies are ready.
)
echo.

REM 3. Train Model or Run Validation if requested
if "%1"=="train" (
    echo [2/3] Force training model now...
    !PYCMD! src\train.py
    if errorlevel 1 (
        echo [ERROR] Failed to train model.
        pause
        exit /b 1
    )
    echo [OK] Model trained successfully.
) else if "%1"=="test" (
    echo [2/3] Running validation suite...
    !PYCMD! src\validate.py
    pause
    exit /b 0
) else if not exist "models\career_classifier.joblib" (
    echo [2/3] Model not found. Training model now...
    !PYCMD! src\train.py
    if errorlevel 1 (
        echo [ERROR] Failed to train model.
        pause
        exit /b 1
    )
    echo [OK] Model trained successfully.
) else (
    echo [2/3] Model is ready: models\career_classifier.joblib
    echo       To force retrain, run: run.bat train
)
echo.

REM 4. Port Conflict Resolution: Free Port 8000 if occupied by lingering background process
for /f "tokens=5" %%p in ('netstat -aon 2^>nul ^| findstr ":8000" ^| findstr "LISTENING"') do (
    echo [INFO] Detected active process on Port 8000 with PID: %%p
    echo [INFO] Terminating previous background instance to ensure clean start...
    taskkill /F /PID %%p >nul 2>&1
    ping 127.0.0.1 -n 2 >nul
)

REM 5. Run FastAPI Server (Auto-opens browser via HTTP once ready)
echo [3/3] Starting backend server and opening web browser...
echo.
!PYCMD! src\main.py

echo.
echo ===================================================
echo [OK] Server stopped.
echo ===================================================
pause