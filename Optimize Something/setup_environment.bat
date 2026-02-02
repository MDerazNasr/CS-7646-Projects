@echo off
REM Setup script for ML4T environment (Windows)
REM This script sets up the Conda environment for the Optimize Something project

echo Setting up ML4T Conda environment...

REM Check if conda is installed
where conda >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Error: Conda is not installed or not in PATH.
    echo Please install Miniconda first.
    echo Download from: https://docs.conda.io/en/latest/miniconda.html
    pause
    exit /b 1
)

REM Create the conda environment from environment.yml
echo Creating conda environment from environment.yml...
call conda env create --file environment.yml

if %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to create conda environment.
    pause
    exit /b 1
)

echo.
echo Setup complete!
echo.
echo To activate the environment, run:
echo   conda activate ml4t
echo.
echo Then, from the "Optimize Something" directory, run your code with:
echo   set PYTHONPATH=../:. && python optimization.py
echo.
echo Or to run the grader:
echo   set PYTHONPATH=../:. && python grade_optimization.py
echo.
pause
