@echo off
REM Build script for Asteroid 2023 BU Orbit Calculation (Simple Version)

echo === Building Asteroid 2023 BU Orbit Calculator (Simple Version) ===

REM Create directories
if not exist Data mkdir Data
if not exist results mkdir results

REM Check if g++ is available
g++ --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: g++ compiler not found!
    echo Please install MinGW-w64 or Visual Studio Build Tools
    echo Download from: https://www.mingw-w64.org/downloads/
    pause
    exit /b 1
)

REM Compile the program (simple version without SOFA)
echo Compiling source files...
g++ -std=c++11 -Wall -O2 -I./src -c src/simple_main.cpp -o src/simple_main.o

if %errorlevel% neq 0 (
    echo Compilation failed!
    pause
    exit /b 1
)

REM Link the program
echo Linking executable...
g++ -std=c++11 -Wall -O2 -I./src -o orbit_calculator_simple.exe src/simple_main.o

if %errorlevel% neq 0 (
    echo Linking failed!
    pause
    exit /b 1
)

echo Build successful!
echo Executable created: orbit_calculator_simple.exe
echo.
echo To run the program: orbit_calculator_simple.exe
echo.
echo Note: This is a simplified version without SOFA library
echo For full functionality, install SOFA and use build.bat
echo.
pause
