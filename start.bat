@echo off
title Free Image-to-3D
cd /d "%~dp0"

echo ========================================
echo   Free Image-to-3D  -  Windows Launcher
echo ========================================
echo.

REM Create venv if it does not exist
if not exist "venv\Scripts\activate.bat" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Failed to create venv. Make sure Python is installed and on PATH.
        pause
        exit /b 1
    )
)

call venv\Scripts\activate

REM Install requirements if needed
if not exist "venv\Lib\site-packages\gradio" (
    echo Installing dependencies...
    pip install -r requirements.txt
)

REM Try to locate or clone TripoSR
set TRIPOSR_DIR=%~dp0TripoSR
if not exist "%TRIPOSR_DIR%\tsr" (
    echo TripoSR not found locally. Attempting to clone...
    git clone https://github.com/VAST-AI-Research/TripoSR.git "%TRIPOSR_DIR%"
)

if exist "%TRIPOSR_DIR%\tsr" (
    set PYTHONPATH=%TRIPOSR_DIR%;%PYTHONPATH%
    echo Using TripoSR from: %TRIPOSR_DIR%
) else (
    echo WARNING: Could not find TripoSR. Mesh generation will fail.
    echo Please clone https://github.com/VAST-AI-Research/TripoSR into the project folder.
)

echo.
echo Starting application...
python app\main.py

echo.
pause
