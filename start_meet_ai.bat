@echo off

title Meet-AI

echo.
echo ========================================
echo            MEET-AI STARTING
echo ========================================
echo.

cd /d "%~dp0"

echo [1/4] Activating Python environment...
call ".venv\Scripts\activate.bat"

if errorlevel 1 (
    echo ERROR: Could not activate virtual environment.
    pause
    exit /b 1
)

echo        OK
echo.

echo [2/4] Checking FFmpeg...

set "FFMPEG_DIR=C:\Program Files\Streamlabs OBS\resources\app.asar.unpacked\node_modules\obs-studio-node"

if not exist "%FFMPEG_DIR%\ffmpeg.exe" (
    echo ERROR: FFmpeg was not found.
    echo.
    echo Expected:
    echo %FFMPEG_DIR%\ffmpeg.exe
    echo.
    pause
    exit /b 1
)

set "PATH=%FFMPEG_DIR%;%PATH%"

echo        FFmpeg found.
echo.

echo [3/4] Checking OpenRouter configuration...

if not exist ".env" (
    echo ERROR: .env file not found.
    echo.
    echo Create a .env file containing:
    echo OPENROUTER_API_KEY=YOUR_API_KEY
    echo.
    pause
    exit /b 1
)

echo        .env found.
echo.

echo [4/4] Starting FastAPI backend...
echo.

uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

echo.
echo ========================================
echo             MEET-AI STOPPED
echo ========================================
echo.

pause