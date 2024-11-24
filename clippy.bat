@echo off
set "VENV_PATH=%~dp0venv"
set "APP_PATH=%~dp0clipboardApp"
set "PID_FILE=%TEMP%\clippy.pid"

if "%1"=="run" (
    echo Starting Clippy...
    cd /d "%APP_PATH%"
    call "%VENV_PATH%\Scripts\activate.bat"
    start /b python main.py
    echo %ERRORLEVEL% > "%PID_FILE%"
    echo Clippy is now running.
    exit /b
)

if "%1"=="stop" (
    echo Stopping Clippy...
    if exist "%PID_FILE%" (
        for /f %%i in (%PID_FILE%) do taskkill /PID %%i /F
        del "%PID_FILE%"
        echo Clippy has been stopped.
    ) else (
        echo Clippy is not running.
    )
    exit /b
)

echo Usage: clippy {run|stop}