@echo off
REM JSON to MySQL Importer - Easy Launch Script
REM This batch file provides a simple way to launch the Python script
REM without needing to use the command line directly

echo ========================================
echo JSON to MySQL Importer
echo ========================================
echo.

REM Check if Python is installed and accessible
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in your PATH
    echo.
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo Python found. Starting application...
echo.

REM Launch the Python script
python JSONtoMySQL.py

REM If Python script exits with an error, show message
if errorlevel 1 (
    echo.
    echo ========================================
    echo Application closed with an error
    echo ========================================
    echo.
    echo If you see import errors, you may need to install requirements:
    echo    pip install -r requirements.txt
    echo.
    echo For other issues, please see README.MD
    echo.
    pause
)

REM Normal exit - no need to pause, window will close automatically