# ML4T Environment Setup for Optimize Something Project

This guide will help you set up the Conda environment for the Optimize Something project.

## Prerequisites

1. **Miniconda** must be installed on your system
   - Download from: https://docs.conda.io/en/latest/miniconda.html
   - Follow the installation instructions for your operating system

2. **Administrative rights** on your local machine

## Setup Steps

### Option 1: Using the Setup Script (Linux/macOS)

1. Make the setup script executable:
   ```bash
   chmod +x setup_environment.sh
   ```

2. Run the setup script:
   ```bash
   ./setup_environment.sh
   ```

### Option 2: Manual Setup

1. **Create the Conda environment:**
   ```bash
   conda env create --file environment.yml
   ```

2. **Activate the environment:**
   ```bash
   conda activate ml4t
   ```

3. **macOS users only** - Configure matplotlib backend (run once):
   ```bash
   mkdir -p ~/.matplotlib
   echo "backend: TkAgg" > ~/.matplotlib/matplotlibrc
   ```

4. **Linux in VirtualBox users only** - Configure matplotlib backend (run once):
   ```bash
   mkdir -p ~/.config/matplotlib
   echo "backend: TkAgg" > ~/.config/matplotlib/matplotlibrc
   ```

## Running Your Code

After activating the environment, navigate to the "Optimize Something" directory and run:

```bash
# Activate the environment first
conda activate ml4t

# Navigate to the project directory
cd "Optimize Something"

# Run your optimization code
PYTHONPATH=../:. python optimization.py

# Or run the grader
PYTHONPATH=../:. python grade_optimization.py
```

## Important Notes

- The `PYTHONPATH=../:.` is required so Python can find `util.py` and the `grading/` directory
- The project structure assumes:
  - `util.py` is in the parent directory (`../`)
  - `data/` folder is in the parent directory (`../data/`)
  - `grading/` folder is in the parent directory (`../grading/`)

## Verifying Your Setup

To verify your environment is set up correctly, you can run the grader:

```bash
conda activate ml4t
cd "Optimize Something"
PYTHONPATH=../:. python grade_optimization.py
```

This will run test cases and generate `points.txt` and `comments.txt` files.

## Troubleshooting

### If conda command is not found:
- Make sure Miniconda is installed
- Restart your terminal after installation
- On macOS/Linux, you may need to initialize conda: `conda init`

### If matplotlib crashes on macOS:
- Make sure you've run the matplotlib backend configuration step
- Try: `mkdir -p ~/.matplotlib && echo "backend: TkAgg" > ~/.matplotlib/matplotlibrc`

### If you get import errors:
- Make sure you're using `PYTHONPATH=../:.` when running scripts
- Verify that `util.py` exists in the parent directory
- Check that the `data/` folder exists in the parent directory

## Environment Details

- **Python Version:** 3.10
- **Key Libraries:**
  - NumPy 1.22.3
  - Pandas 1.4.3
  - SciPy 1.7.3
  - Matplotlib 3.5
  - PyTest 7.1.2

For more details, see the `environment.yml` file.
