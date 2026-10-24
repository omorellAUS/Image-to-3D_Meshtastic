@echo off
setlocal enabledelayedexpansion

echo ========================================
echo   Free Image-to-3D  -  Windows Launcher
echo   (CUDA GPU build)
echo ========================================

cd /d "%~dp0"

if not exist "venv\Scripts\activate.bat" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Failed to create venv. Make sure Python 3.10 is on PATH.
        pause
        exit /b 1
    )
)

call venv\Scripts\activate.bat

echo.
echo Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Cleaning any previous torch packages...
pip uninstall torch torchvision torchmcubes -y >nul 2>&1

echo.
echo Installing CUDA 12.4 PyTorch...
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124 --force-reinstall
if errorlevel 1 (
    echo CUDA torch install failed.
    pause
    exit /b 1
)

echo.
echo Verifying CUDA...
python -c "import torch; print('Torch:', torch.__version__); print('CUDA available:', torch.cuda.is_available()); print('Device:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU')"
if errorlevel 1 (
    echo CUDA verification failed.
    pause
    exit /b 1
)

echo.
echo Installing remaining dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo requirements.txt install failed.
    pause
    exit /b 1
)

echo.
echo Building torchmcubes (no torch reinstall)...
pip install --no-build-isolation --no-deps git+https://github.com/tatsy/torchmcubes.git
if errorlevel 1 (
    echo torchmcubes build failed.
    echo Make sure Visual Studio C++ tools and CUDA 12.4 are installed.
    pause
    exit /b 1
)

echo.
echo Re-checking CUDA after torchmcubes...
python -c "import torch; print('Torch:', torch.__version__); print('CUDA available:', torch.cuda.is_available())"

echo.
echo Checking TripoSR folder...
if not exist "TripoSR\tsr\system.py" (
    echo Cloning TripoSR...
    git clone https://github.com/VAST-AI-Research/TripoSR.git
)

echo.
echo Starting application...
python app\main.py

pause