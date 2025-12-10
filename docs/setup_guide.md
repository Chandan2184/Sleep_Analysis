# Setup Guide

## Initial Setup

### 1. Prerequisites

Ensure you have Python 3.7 or higher installed:
```bash
python3 --version
```

### 2. Clone/Download Project

If using git:
```bash
git clone [repository-url]
cd Sleep_Quality_Analysis
```

Or extract the project folder to your desired location.

### 3. Create Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Add Data Files

Place all NHANES `.xpt` files in the `data/raw/` directory:
- ALQ_J.xpt
- BPQ_J.xpt
- DEMO_J.xpt
- DPQ_J.xpt
- SLQ_J.xpt
- SMQ_J.xpt

### 6. Verify Setup

Check that all files are in place:
```bash
ls data/raw/*.xpt
```

You should see all 6 files listed.

---

## Running the Analysis

### Option 1: Run Complete Pipeline

```bash
python scripts/run_all_analysis.py
```

This will execute all analysis steps sequentially.

### Option 2: Run Steps Individually

```bash
# Step 1: Prepare data
python scripts/01_prepare_data.py

# Step 2: K-means clustering
python scripts/02_clustering.py

# Step 3: Linear regression
python scripts/03_regression.py

# Step 4: Decision trees
python scripts/04_decision_trees.py
```

---

## Project Structure

After running the analysis, your project structure will be:

```
Sleep_Quality_Analysis/
├── data/
│   ├── raw/              # Original .xpt files
│   └── processed/        # Cleaned dataset (after Step 1)
├── results/
│   ├── figures/          # All plots and visualizations
│   ├── tables/           # Summary tables and coefficients
│   └── models/           # Saved models (if applicable)
├── scripts/              # Analysis scripts
└── docs/                 # Documentation
```

---

## Troubleshooting

### Issue: ModuleNotFoundError

**Solution:** Ensure virtual environment is activated and dependencies are installed:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: FileNotFoundError for .xpt files

**Solution:** Ensure all .xpt files are in `data/raw/` directory:
```bash
ls data/raw/
```

### Issue: Missing results directory

**Solution:** The scripts will create the results directory automatically. If errors occur, create manually:
```bash
mkdir -p results/figures results/tables results/models
```

### Issue: Import errors

**Solution:** Ensure you're running scripts from the project root or using the correct Python path:
```bash
cd Sleep_Quality_Analysis
python scripts/01_prepare_data.py
```

---

## Next Steps

After successful setup and execution:

1. **Review Results:** Check `results/figures/` and `results/tables/`
2. **Read Documentation:** See `docs/project_report.md` for interpretation
3. **Modify Analysis:** Edit scripts in `scripts/` as needed
4. **Write Report:** Use `docs/project_report.md` as template

---

## Getting Help

If you encounter issues:

1. Check error messages carefully
2. Verify all files are in correct locations
3. Ensure Python version is compatible
4. Check that all dependencies are installed
5. Review the README.md for project overview

