@echo off
REM Build script for Asteroid 2023 BU Orbit Calculation

echo === Building Asteroid 2023 BU Orbit Calculator ===

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

REM Compile the program
echo Compiling source files...
g++ -std=c++11 -Wall -O2 -I./src -c src/main.cpp -o src/main.o

if %errorlevel% neq 0 (
    echo Compilation failed!
    pause
    exit /b 1
)

REM Link the program
echo Linking executable...
g++ -std=c++11 -Wall -O2 -I./src -o orbit_calculator.exe src/main.o

if %errorlevel% neq 0 (
    echo Linking failed!
    echo Note: You may need to install SOFA library
    echo Download from: http://www.iausofa.org/
    pause
    exit /b 1
)

echo Build successful!
echo Executable created: orbit_calculator.exe
echo.
echo To run the program: orbit_calculator.exe
echo.
pause
