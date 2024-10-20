@echo off
setlocal

REM Check if Python is installed
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed on your system.
    echo Please install Python and try running this script again.
    pause
    exit /b 1
)

echo Python is installed. Proceeding...

REM Check if pip is available
pip --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Pip is not installed or not found in PATH.
    echo Please ensure pip is installed and added to your PATH.
    pause
    exit /b 1
)

echo Pip is available. Installing requirements...

REM Install the packages from requirements.txt
pip install -r requirements.txt

IF %ERRORLEVEL% NEQ 0 (
    echo Failed to install one or more packages.
    echo Please check the error message above for details.
    pause
    exit /b 1
)

echo All packages installed successfully.
python voc.py
exit /b 0
