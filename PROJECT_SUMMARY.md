# Project Summary: Sleep Quality Analysis

## Quick Overview

**Project Name:** Sleep Quality Analysis - Effects of Smoking and Alcohol Consumption

**Objective:** Analyze how smoking and alcohol consumption affect sleep quality using three machine learning approaches.

**Dataset:** NHANES 2017-2018 (5,533 participants)

**Methods:**
- ✅ K-Means Clustering
- ✅ Linear Regression
- ✅ Decision Trees

---

## What's Included

### 📁 Project Structure
```
Sleep_Quality_Analysis/
├── README.md              # Main project documentation
├── requirements.txt       # Python dependencies
├── data/                  # Data files
├── src/                   # Source code modules
├── scripts/               # Execution scripts
├── results/               # Analysis outputs
└── docs/                  # Documentation
```

### 📊 Analysis Scripts
1. `01_prepare_data.py` - Data loading, cleaning, merging
2. `02_clustering.py` - K-means clustering analysis
3. `03_regression.py` - Linear regression models
4. `04_decision_trees.py` - Decision tree analysis
5. `run_all_analysis.py` - Complete pipeline

### 📝 Documentation
- `README.md` - Project overview and instructions
- `docs/project_report.md` - Comprehensive project report template
- `docs/methodology.md` - Detailed methodology
- `docs/variable_selection.md` - Variable selection guide
- `docs/setup_guide.md` - Setup instructions

---

## Quick Start

1. **Setup:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Add Data:**
   - Place .xpt files in `data/raw/`

3. **Run Analysis:**
   ```bash
   python scripts/run_all_analysis.py
   ```

4. **Review Results:**
   - Check `results/figures/` for visualizations
   - Check `results/tables/` for summary statistics
   - See `docs/project_report.md` for interpretation

---

## Key Features

✅ **Modular Code Structure** - Organized, reusable modules  
✅ **Complete Pipeline** - End-to-end analysis workflow  
✅ **Comprehensive Documentation** - Ready for submission  
✅ **Reproducible** - All scripts and requirements included  
✅ **Professional Output** - Publication-quality figures and tables  

---

## Expected Deliverables

After running the analysis, you'll have:

1. **Prepared Dataset** (`data/processed/prepared_sleep_analysis_data.csv`)
2. **Clustering Results** (cluster characteristics, visualizations)
3. **Regression Models** (coefficients, R², diagnostic plots)
4. **Decision Trees** (tree diagrams, feature importance, rules)
5. **All Figures** (saved as PNG files)
6. **Summary Tables** (saved as CSV files)

---

## For College Submission

This project includes:

✅ **Complete Code** - Well-organized, commented, modular  
✅ **Documentation** - README, methodology, setup guide  
✅ **Report Template** - Ready to fill with your results  
✅ **Professional Structure** - Industry-standard organization  
✅ **Reproducible Analysis** - All dependencies specified  

**What You Need to Do:**

1. Run the analysis scripts
2. Fill in results in `docs/project_report.md`
3. Add your name, course, date
4. Review and customize as needed
5. Submit!

---

## File Checklist

Before submission, ensure:

- [ ] All .xpt files in `data/raw/`
- [ ] Analysis scripts run successfully
- [ ] Results generated in `results/` directory
- [ ] `docs/project_report.md` filled with results
- [ ] README.md reviewed and updated
- [ ] Your name/course/date added to documentation
- [ ] Code runs on clean environment (test this!)

---

## Questions?

Refer to:
- `README.md` for project overview
- `docs/setup_guide.md` for setup issues
- `docs/methodology.md` for methodology questions
- `docs/variable_selection.md` for variable information

---

**Last Updated:** [Date]  
**Project Status:** Ready for Analysis

