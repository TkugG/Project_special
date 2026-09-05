@echo off
setlocal
cd /d "%~dp0"

title AI Job Matcher - Startup

echo ===================================================
echo           AI Job Matcher - ML Backend
echo ===================================================
echo.

REM 1. Check Python
where python >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.8+ and add it to PATH.
    pause
    exit /b 1
)

for /f "tokens=*" %%v in ('python --version 2^>^&1') do set PYVER=%%v
echo [OK] Found %PYVER%
echo.

REM 2. Install Dependencies
echo [1/3] Checking dependencies...
pip install -r requirements.txt -q --disable-pip-version-check
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies from requirements.txt
    pause
    exit /b 1
)
echo [OK] Dependencies are ready.
echo.

REM 3. Train Model if missing
if not exist "models\career_classifier.joblib" (
    echo [2/3] models\career_classifier.joblib not found. Training model now...
    python src\train.py
    if errorlevel 1 (
        echo [ERROR] Failed to train model.
        pause
        exit /b 1
    )
    echo [OK] Model trained successfully.
) else (
    echo [2/3] models\career_classifier.joblib exists. Skipping training.
)
echo.

REM 4. Open index.html in browser
echo [3/3] Opening index.html in default browser...
start "" "%~dp0index.html"

REM 5. Run FastAPI Server
echo.
echo ===================================================
echo  Server is running at: http://127.0.0.1:8000
echo  Press Ctrl+C in this window to stop the server.
echo ===================================================
echo.
python src\main.py

pause