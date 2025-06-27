@echo off
title Parakeet-Writer Launcher
echo ================================================================
echo                    Parakeet-Writer Launcher
echo ================================================================
echo.

REM Check if we're in the right directory
if not exist "run_whisperwriter_parakeet.py" (
    echo ERROR: Please run this script from the Parakeet-Writer directory
    echo Looking for: run_whisperwriter_parakeet.py
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv_parakeet_py311\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run 'install.bat' first to set up the environment.
    pause
    exit /b 1
)

echo Starting Parakeet-Writer...
echo.

REM Activate virtual environment
echo [1/3] Activating virtual environment...
call venv_parakeet_py311\Scripts\activate.bat

REM Start Parakeet server for optimal performance
echo [2/3] Starting Parakeet server for fast transcription...
start /B python whisper-writer-parakeet\parakeet_server.py

REM Wait a moment for server to initialize
echo [3/3] Starting Parakeet-Writer application...
echo.
echo ----------------------------------------------------------------
echo                        IMPORTANT NOTES:
echo ----------------------------------------------------------------
echo • First run may take 1-2 minutes due to model downloading
echo • GPU acceleration enabled for fast transcription
echo • Use ONLY safe settings (see documentation)
echo • Server mode provides 1-2 second transcription speed
echo ----------------------------------------------------------------
echo.

REM Small delay to let server start
timeout /t 2 /nobreak >nul

REM Start the main application
python run_whisperwriter_parakeet.py

REM Cleanup message
echo.
echo ================================================================
echo Parakeet-Writer has closed.
echo Press any key to exit...
pause >nul 