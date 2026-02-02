#!/bin/bash
# Setup script for ML4T environment
# This script sets up the Conda environment for the Optimize Something project

echo "Setting up ML4T Conda environment..."

# Check if conda is installed
if ! command -v conda &> /dev/null; then
    echo "Error: Conda is not installed. Please install Miniconda first."
    echo "Download from: https://docs.conda.io/en/latest/miniconda.html"
    exit 1
fi

# Create the conda environment from environment.yml
echo "Creating conda environment from environment.yml..."
conda env create --file environment.yml

# Activate the environment
echo "Activating ml4t environment..."
echo ""
echo "To activate the environment, run:"
echo "  conda activate ml4t"
echo ""
echo "Then, from the 'Optimize Something' directory, run your code with:"
echo "  PYTHONPATH=../:. python optimization.py"
echo ""
echo "Or to run the grader:"
echo "  PYTHONPATH=../:. python grade_optimization.py"
echo ""

# macOS fix for matplotlib (if on macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Detected macOS. Setting up matplotlib backend..."
    mkdir -p ~/.matplotlib
    echo "backend: TkAgg" > ~/.matplotlib/matplotlibrc
    echo "Matplotlib backend configured for macOS."
fi

echo "Setup complete!"
