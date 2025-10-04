@echo off
REM Quick start script for Asteroid 2023 BU Orbit Calculation

echo === Asteroid 2023 BU Orbit Calculation ===
echo Setting up project...

REM Create directories
if not exist Data mkdir Data
if not exist results mkdir results

REM Download data if Python is available
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Downloading real data from MPC and JPL...
    python download_data.py
) else (
    echo Python not found. Using sample data.
    echo To download real data, install Python and run: python download_data.py
)

REM Build the project
echo Building project...
make setup
make

if %errorlevel% equ 0 (
    echo Build successful!
    echo Running orbit calculation...
    make run
) else (
    echo Build failed! Please check the error messages above.
    echo Make sure you have:
    echo 1. C++ compiler (g++)
    echo 2. SOFA library installed
    echo 3. All source files in place
)

pause
