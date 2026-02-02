# Quick Start Guide

## First Time Setup

1. **Install Miniconda** (if not already installed)
   - Download: https://docs.conda.io/en/latest/miniconda.html

2. **Create the Conda environment:**
   ```bash
   # Linux/macOS
   ./setup_environment.sh
   
   # OR manually:
   conda env create --file environment.yml
   ```

   ```cmd
   REM Windows
   setup_environment.bat
   
   REM OR manually:
   conda env create --file environment.yml
   ```

3. **Activate the environment:**
   ```bash
   conda activate ml4t
   ```

## Running Your Code

**Always activate the environment first:**
```bash
conda activate ml4t
```

**Then run from the "Optimize Something" directory:**

```bash
# Run your optimization code
PYTHONPATH=../:. python optimization.py

# Run the grader
PYTHONPATH=../:. python grade_optimization.py
```

**Windows users:**
```cmd
set PYTHONPATH=../:. && python optimization.py
set PYTHONPATH=../:. && python grade_optimization.py
```

## Important Notes

- ✅ Always use `PYTHONPATH=../:.` to find `util.py` and `grading/`
- ✅ The environment must be activated before running code
- ✅ Make sure you're in the "Optimize Something" directory when running scripts

## Directory Structure

Your project should have this structure:
```
CS-7646-Projects/
├── data/              (stock CSV files)
├── grading/           (grading utilities)
├── util.py            (utility functions)
└── Optimize Something/
    ├── optimization.py
    ├── grade_optimization.py
    ├── environment.yml
    └── ...
```
