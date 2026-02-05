@echo off
REM Setup script for ML CSV Automation Project
REM Windows PowerShell version

echo ============================================
echo ML CSV Automation - Setup Script
echo ============================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/5] Python found: 
python --version
echo.

REM Create virtual environment (optional)
echo [2/5] Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed successfully!
echo.

REM Create necessary directories
echo [3/5] Creating directories...
mkdir data >nul 2>&1
mkdir models >nul 2>&1
mkdir output >nul 2>&1
mkdir logs >nul 2>&1
echo Directories created!
echo.

REM Copy .env file
echo [4/5] Setting up configuration...
if not exist .env (
    copy .env.example .env >nul 2>&1
    echo .env file created. Please update with your configuration.
) else (
    echo .env file already exists.
)
echo.

REM Run tests
echo [5/5] Running tests...
python -m unittest tests.py 2>nul
if errorlevel 1 (
    echo WARNING: Some tests failed. Check logs.
) else (
    echo Tests passed!
)
echo.

echo ============================================
echo Setup Complete!
echo ============================================
echo.
echo Next steps:
echo 1. Place your training data in: data/train.csv
echo 2. Place your test data in: data/test.csv
echo 3. Run the project:
echo    - Command line: python main.py
echo    - Web API: python app.py (then visit http://localhost:5000)
echo.
echo For more information, see README.md
echo.
pause
