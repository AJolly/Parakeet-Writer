@echo off
echo ================================================================
echo                 Parakeet-Writer Installation Script
echo ================================================================
echo.

REM Check if we're in the right directory
if not exist "run_whisperwriter_parakeet.py" (
    echo ERROR: Please run this script from the Parakeet-Writer directory
    echo Make sure you see these files: run_whisperwriter_parakeet.py, requirements.txt
    pause
    exit /b 1
)

echo Step 1: Checking Python 3.11 availability...
py -3.11 --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: Python 3.11 is required but not found!
    echo Please install Python 3.11 first:
    echo   winget install Python.Python.3.11
    echo.
    echo WARNING: Python 3.13+ is NOT compatible with this project!
    pause
    exit /b 1
)
echo ✓ Python 3.11 found

echo.
echo Step 2: Creating virtual environment...
if exist "venv_parakeet_py311" (
    echo Virtual environment already exists. Removing old one...
    rmdir /s /q venv_parakeet_py311
)
py -3.11 -m venv venv_parakeet_py311
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)
echo ✓ Virtual environment created

echo.
echo Step 3: Activating virtual environment...
call venv_parakeet_py311\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo ✓ Virtual environment activated

echo.
echo Step 4: Upgrading pip...
python -m pip install --upgrade pip
echo ✓ Pip upgraded

echo.
echo Step 5: Installing PyTorch with CUDA support...
echo This may take several minutes...
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu121
if errorlevel 1 (
    echo ERROR: Failed to install PyTorch
    pause
    exit /b 1
)
echo ✓ PyTorch installed

echo.
echo Step 6: Installing remaining dependencies...
echo This may take several minutes...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    echo Trying individual installation...
    pip install omegaconf hydra-core
    pip install nemo-toolkit[asr]
    pip install webrtcvad python-dotenv openai
    pip install PyQt5 pynput audioplayer sounddevice scipy
    pip install cuda-python
)
echo ✓ Dependencies installed

echo.
echo Step 7: Testing installation...
python -c "import torch; print('CUDA available:', torch.cuda.is_available())"
python -c "import nemo; print('NeMo installed successfully')"
if errorlevel 1 (
    echo WARNING: Installation test failed, but continuing...
)

echo.
echo ================================================================
echo                    Installation Complete!
echo ================================================================
echo.
echo Next steps:
echo 1. Double-click 'start.bat' to run Parakeet-Writer
echo 2. Or manually run: python run_whisperwriter_parakeet.py
echo.
echo First run will be slower due to model downloading.
echo Use only 'safe' settings as mentioned in documentation.
echo.
pause 