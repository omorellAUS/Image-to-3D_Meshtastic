@echo off
title Free Image-to-3D
cd /d "%~dp0"

echo ========================================
echo   Free Image-to-3D  -  Windows Launcher
echo ========================================
echo.

if not exist "venv\Scripts\activate.bat" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Python not found. Install Python 3.10 or 3.11 from python.org and add it to PATH.
        pause
        exit /b 1
    )
)

call venv\Scripts\activate

if not exist "venv\Lib\site-packages\gradio" (
    echo Installing dependencies...
    pip install -r requirements.txt
)

set TRIPOSR_DIR=%~dp0TripoSR
if not exist "%TRIPOSR_DIR%\tsr" (
    echo TripoSR not found. Attempting to clone...
    git clone https://github.com/VAST-AI-Research/TripoSR.git "%TRIPOSR_DIR%"
)

if exist "%TRIPOSR_DIR%\tsr" (
    set PYTHONPATH=%TRIPOSR_DIR%;%PYTHONPATH%
    echo Using TripoSR from: %TRIPOSR_DIR%
) else (
    echo WARNING: TripoSR missing. Clone it into the project folder or install Git.
)

echo.
echo Starting application...
python app\main.py

echo.
pause
