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
if not exist "venv_parakeet\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run 'install.bat' first to set up the environment.
    pause
    exit /b 1
)

echo Starting Parakeet-Writer...
echo.

REM Activate virtual environment
echo [1/3] Activating virtual environment...
call venv_parakeet\Scripts\activate.bat

REM Check if Parakeet server is already running
echo [2/3] Checking Parakeet server status...
REM Method 1: Check for python processes with parakeet_server.py in command line
wmic process where "name='python.exe' and commandline like '%parakeet_server.py%'" get processid 2>nul | find /I "ProcessId" >nul
if %errorlevel% equ 0 (
    echo [2/3] ✓ Parakeet server is already running - skipping server start
    set SERVER_RUNNING=1
) else (
    REM Fallback method: Check for any python process in the whisper-writer-parakeet directory
    tasklist /FI "IMAGENAME eq python.exe" /FO CSV 2>nul | find /I "whisper-writer-parakeet" >nul
    if %errorlevel% equ 0 (
        echo [2/3] ✓ Found existing Python process in Parakeet directory - assuming server is running
        set SERVER_RUNNING=1
    ) else (
        echo [2/3] → Starting Parakeet server for fast transcription...
        start "Parakeet Server" /B python whisper-writer-parakeet\parakeet_server.py
        if %errorlevel% equ 0 (
            echo [2/3] ✓ Server started successfully
            set SERVER_RUNNING=0
            REM Wait a moment for server to initialize
            timeout /t 2 /nobreak >nul
        ) else (
            echo [2/3] ⚠ Warning: Server start may have failed, but continuing...
            set SERVER_RUNNING=0
        )
    )
)

REM Start the main application
echo [3/3] Starting Parakeet-Writer application...
echo.
echo ----------------------------------------------------------------
echo                        IMPORTANT NOTES:
echo ----------------------------------------------------------------
echo â€¢ First run may take 1-2 minutes due to model downloading
echo â€¢ GPU acceleration enabled for fast transcription
echo â€¢ Use ONLY safe settings (see documentation)
echo â€¢ Server mode provides 1-2 second transcription speed
echo ----------------------------------------------------------------
echo.

REM Small delay only if we just started a new server
if %SERVER_RUNNING% equ 0 (
    echo Waiting for server to initialize...
    timeout /t 2 /nobreak >nul
) else (
    echo Server already running - proceeding immediately...
)

REM Display server status summary
echo.
echo ----------------------------------------------------------------
echo                        SERVER STATUS:
echo ----------------------------------------------------------------
if %SERVER_RUNNING% equ 1 (
    echo ✓ Using existing Parakeet server instance
) else (
    echo ✓ Started new Parakeet server instance
)
echo ----------------------------------------------------------------
echo.

REM Start the main application
python run_whisperwriter_parakeet.py

REM Cleanup message
echo.
echo ================================================================
echo Parakeet-Writer has closed.
if %SERVER_RUNNING% equ 0 (
    echo Note: Parakeet server is still running in the background.
    echo To stop the server, close the python.exe process or restart your computer.
) else (
    echo Note: Using existing Parakeet server - no cleanup needed.
)
echo Press any key to exit...
pause >nul 