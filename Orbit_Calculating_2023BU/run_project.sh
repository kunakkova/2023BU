#!/bin/bash
# Quick start script for Asteroid 2023 BU Orbit Calculation

echo "=== Asteroid 2023 BU Orbit Calculation ==="
echo "Setting up project..."

# Create directories
mkdir -p Data results

# Download data if Python is available
if command -v python3 &> /dev/null; then
    echo "Downloading real data from MPC and JPL..."
    python3 download_data.py
else
    echo "Python3 not found. Using sample data."
    echo "To download real data, install Python3 and run: python3 download_data.py"
fi

# Build the project
echo "Building project..."
make setup
make

if [ $? -eq 0 ]; then
    echo "Build successful!"
    echo "Running orbit calculation..."
    make run
else
    echo "Build failed! Please check the error messages above."
    echo "Make sure you have:"
    echo "1. C++ compiler (g++)"
    echo "2. SOFA library installed"
    echo "3. All source files in place"
fi
