# Sleep Quality Analysis: Effects of Smoking and Alcohol Consumption


## 📋 Project Overview

This project investigates the relationships between **smoking**, **alcohol consumption**, and **sleep quality** using machine learning techniques. The analysis employs three complementary approaches:

1. **K-Means Clustering** - Unsupervised learning to identify lifestyle groups
2. **Linear Regression** - Supervised learning to quantify relationships
3. **Decision Trees** - Supervised learning to identify key predictors and decision rules

### Research Question
*How do smoking and alcohol consumption patterns affect sleep quality, and can we predict sleep outcomes using lifestyle factors?*

---

## 📁 Project Structure

```
Sleep_Quality_Analysis/
├── README.md                    # This file
├── PROJECT_SUMMARY.md           # Quick project overview
├── requirements.txt             # Python dependencies
├── verify_setup.py              # Setup verification script
├── run_analysis.py              # Alternative analysis runner
├── EXECUTE_ANALYSIS.sh          # Bash script for complete pipeline
├── data/
│   ├── raw/                     # Original NHANES files (.xpt)
│   └── processed/               # Cleaned and merged datasets
├── src/
│   ├── data_prep/               # Data preparation modules
│   │   ├── __init__.py
│   │   ├── load_data.py         # Load and merge datasets
│   │   ├── clean_data.py        # Data cleaning functions
│   │   └── feature_engineering.py  # Create derived variables
│   └── analysis/                # Analysis modules
│       ├── __init__.py
│       ├── clustering.py        # K-means clustering
│       ├── regression.py        # Linear regression models
│       └── decision_trees.py    # Decision tree analysis
├── notebooks/                   # Jupyter notebooks (optional)
├── scripts/                     # Main execution scripts
│   ├── 01_prepare_data.py       # Step 1: Prepare data
│   ├── 02_clustering.py         # Step 2: K-means analysis
│   ├── 03_regression.py         # Step 3: Regression models
│   ├── 04_decision_trees.py     # Step 4: Decision trees
│   └── run_all_analysis.py      # Run complete analysis pipeline
├── results/
│   ├── figures/                 # All generated plots
│   ├── tables/                  # Summary tables
│   └── models/                  # Saved model objects
└── docs/
    ├── project_report.md        # Comprehensive project report
    ├── methodology.md           # Detailed methodology
    ├── variable_selection.md    # Variable selection guide
    └── setup_guide.md           # Detailed setup instructions
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Installation

1. **Clone or download this project**

2. **Create a virtual environment (recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Add NHANES data files to `data/raw/`:**
   - Copy all `.xpt` files to `data/raw/`
   - Files needed: ALQ_J.xpt, BPQ_J.xpt, DEMO_J.xpt, DPQ_J.xpt, SLQ_J.xpt, SMQ_J.xpt
   - **Note:** Data files are already in place if you used the project structure

5. **Verify setup (optional but recommended):**
   ```bash
   python verify_setup.py
   ```
   This will check that all files, directories, and packages are correctly installed.

### Running the Analysis

**Option 1: Run complete pipeline (Recommended)**
```bash
python scripts/run_all_analysis.py
```

**Option 2: Run using bash script**
```bash
chmod +x EXECUTE_ANALYSIS.sh
./EXECUTE_ANALYSIS.sh
```

**Option 3: Run step-by-step**
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

**Option 4: Use alternative runner**
```bash
python run_analysis.py
```

---

## 📊 Results

All results are saved in the `results/` directory:

- **Figures:** Visualizations (cluster plots, regression diagnostics, tree diagrams)
- **Tables:** Summary statistics, model coefficients, performance metrics
- **Models:** Saved model objects for reproducibility

---

## 📝 Key Findings

### 1. Lifestyle Clusters
[Summary of identified clusters and their characteristics]

### 2. Regression Results
[Key coefficients and significance levels]

### 3. Decision Tree Insights
[Important predictors and decision rules]

---

## 🛠️ Technologies Used

- **Python 3.7+** - Programming language
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computations
- **Scikit-learn** - Machine learning (K-means, regression, decision trees)
- **Statsmodels** - Statistical modeling and regression analysis
- **Matplotlib/Seaborn** - Data visualization
- **Pyreadstat** - Reading SAS transport files (.xpt)

---

## 📚 Documentation

- **Project Report:** `docs/project_report.md` - Comprehensive analysis report template
- **Methodology:** `docs/methodology.md` - Detailed methodology and approach
- **Variable Selection:** `docs/variable_selection.md` - Complete variable selection guide
- **Setup Guide:** `docs/setup_guide.md` - Detailed setup instructions and troubleshooting
- **Project Summary:** `PROJECT_SUMMARY.md` - Quick reference guide

---

## 🔬 Research Questions Addressed

1. How does smoking status affect sleep quality and duration?
2. How does alcohol consumption affect sleep patterns?
3. Is there an interaction effect between smoking and alcohol on sleep?
4. What lifestyle clusters exist in the population?
5. Which factors are most important in predicting poor sleep quality?
6. What are the decision rules for identifying at-risk individuals?

---

## ⚠️ Limitations

- Cross-sectional data limits causal inference (associations only)
- Missing data requires careful handling
- Self-reported measures may introduce bias
- Complex survey weights needed for population-level estimates

## 🔧 Troubleshooting

### Common Issues

**Issue: ModuleNotFoundError**
- **Solution:** Ensure virtual environment is activated and dependencies installed:
  ```bash
  source venv/bin/activate
  pip install -r requirements.txt
  ```

**Issue: FileNotFoundError for .xpt files**
- **Solution:** Verify all .xpt files are in `data/raw/`:
  ```bash
  ls data/raw/*.xpt
  ```

**Issue: Import errors when running scripts**
- **Solution:** Run scripts from the project root directory:
  ```bash
  cd Sleep_Quality_Analysis
  python scripts/01_prepare_data.py
  ```

**Issue: Missing results directory**
- **Solution:** Scripts create this automatically, but you can create manually:
  ```bash
  mkdir -p results/figures results/tables results/models
  ```

For more detailed troubleshooting, see `docs/setup_guide.md`.

## ✅ Verification

Before running analysis, verify your setup:
```bash
python verify_setup.py
```

This will check:
- ✓ All required directories exist
- ✓ All Python modules are in place
- ✓ Data files are present
- ✓ Required packages are installed

---

## 📄 License

[Add your license or citation information]

---

## 👥 Acknowledgments

- NHANES for providing the data
- Course instructors for guidance
- [Add other acknowledgments]

---

## 📧 Contact

[Your email or contact information]

---

## 📍 Project Location

**Full Path:**
```
/Users/chandinikalluri/Downloads/attachments/Sleep_Quality_Analysis
```

Navigate to the project:
```bash
cd /Users/chandinikalluri/Downloads/attachments/Sleep_Quality_Analysis
```

---

**Last Updated:** December 2024  
**Project Status:** ✅ Ready for Analysis

