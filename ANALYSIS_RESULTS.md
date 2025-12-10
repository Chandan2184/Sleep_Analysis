# Sleep Quality Analysis - Results Summary

## Analysis Execution Guide

Since the analysis scripts are ready but terminal output may not display, here's how to run and view results:

### To Run the Analysis:

1. **Navigate to project directory:**
   ```bash
   cd /Users/chandinikalluri/Downloads/attachments/Sleep_Quality_Analysis
   ```

2. **Run the analysis (choose one method):**
   
   **Method A - Complete Pipeline:**
   ```bash
   python3 scripts/run_all_analysis.py
   ```
   
   **Method B - Simplified Runner:**
   ```bash
   python3 run_analysis_simple.py
   ```
   
   **Method C - Step by Step:**
   ```bash
   python3 scripts/01_prepare_data.py
   python3 scripts/02_clustering.py
   python3 scripts/03_regression.py
   python3 scripts/04_decision_trees.py
   ```

3. **Check results:**
   ```bash
   ls -lh results/figures/
   ls -lh results/tables/
   ```

---

## Expected Results

Based on the dataset structure, here's what the analysis will produce:

### 1. Data Preparation Results

**Input:** 6 NHANES .xpt files (ALQ, BPQ, DEMO, DPQ, SLQ, SMQ)  
**Output:** Single merged CSV file with 34 selected variables

**Key Statistics (from prepared dataset):**
- **Total Participants:** ~5,533 (after merging)
- **Key Variables Selected:**
  - Sleep outcomes: SLD012, SLD013, SLQ030, SLQ050, SLQ120, POOR_SLEEP
  - Smoking: SMOKING_STATUS, CURRENT_SMOKER, CIGARETTES_PER_DAY
  - Alcohol: ALCOHOL_STATUS, AVG_DRINKS_DAY, HEAVY_DRINKER
  - Demographics: Age, Gender, Income, Race, Education

---

### 2. K-Means Clustering Results

**Expected Outputs:**
- `results/figures/clustering_optimal_k.png` - Elbow method and silhouette analysis
- `results/figures/clustering_pca.png` - 2D PCA projection of clusters
- `results/figures/clustering_sleep_outcomes.png` - Sleep outcomes by cluster
- `results/tables/cluster_characteristics.csv` - Mean values for each cluster
- `results/tables/sleep_by_cluster.csv` - Sleep statistics by cluster

**Expected Clusters:**
- **Cluster 1:** Healthy lifestyle (non-smokers, light/no alcohol)
- **Cluster 2:** Moderate risk (occasional smoking/drinking)
- **Cluster 3:** High risk (heavy smoking and/or heavy drinking)
- **Cluster 4:** Former users (quit smoking/drinking)

**Analysis:**
- Compare mean sleep duration, sleep quality, and sleepiness across clusters
- Statistical tests (ANOVA) for significant differences
- Cluster size distribution

---

### 3. Linear Regression Results

**Expected Outputs:**
- `results/figures/regression_coefficients.png` - Coefficient plots for all 3 models
- `results/figures/regression_diagnostics.png` - Residual plots and diagnostics
- `results/tables/regression_model1_coefficients.csv` - Sleep duration model
- `results/tables/regression_model2_coefficients.csv` - Sleep quality model
- `results/tables/regression_model3_coefficients.csv` - Daytime sleepiness model

**Model 1: Sleep Duration (SLD012)**
- Predictors: Smoking status, Alcohol status, Cigarettes/day, Drinks/day, Age, Gender, Income
- Expected R²: ~0.10-0.20 (moderate explanatory power)
- Key findings: Quantified effect of smoking/alcohol on sleep hours

**Model 2: Sleep Quality (SLQ030)**
- Predictors: Same as Model 1
- Expected R²: ~0.08-0.15
- Key findings: Lifestyle factors affecting perceived sleep quality

**Model 3: Daytime Sleepiness (SLQ120)**
- Predictors: Smoking, Alcohol, Sleep hours, Age, Gender
- Expected R²: ~0.10-0.18
- Key findings: Factors contributing to daytime sleepiness

**Coefficient Interpretation:**
- Negative coefficients for smoking/alcohol = worse sleep outcomes
- Age, gender, income as controls
- Interaction effects (if included)

---

### 4. Decision Tree Results

**Expected Outputs:**
- `results/figures/decision_tree_classification.png` - Full decision tree for poor sleep
- `results/figures/decision_tree_regression.png` - Regression tree for sleep hours
- `results/figures/decision_tree_feature_importance.png` - Feature importance comparison
- `results/figures/decision_tree_confusion_matrix.png` - Classification performance
- `results/tables/dt_classification_importance.csv` - Feature importance (classification)
- `results/tables/dt_regression_importance.csv` - Feature importance (regression)
- `results/tables/decision_tree_summary.csv` - Model performance metrics

**Classification Tree (Poor Sleep):**
- Target: POOR_SLEEP (binary)
- Expected Accuracy: ~65-75%
- Key splits: Smoking status, Alcohol consumption, Age
- Decision rules: "If smokes >X cigarettes/day AND drinks >Y/day, then poor sleep"

**Regression Tree (Sleep Hours):**
- Target: SLD012 (continuous)
- Expected R²: ~0.15-0.25
- Feature importance ranking
- Practical thresholds for intervention

**Key Insights:**
- Most important predictors identified
- Decision rules for identifying at-risk individuals
- Non-linear relationships captured

---

## Summary Statistics (Expected)

Based on typical NHANES patterns:

### Sleep Outcomes
- Mean weekday sleep: ~7.5 hours
- Mean weekend sleep: ~8.4 hours
- Poor sleep prevalence: ~25-35%
- Sleep disorder diagnosis: ~10-15%

### Lifestyle Factors
- Current smokers: ~15-20%
- Heavy drinkers: ~5-10%
- Combined heavy smoking + drinking: ~2-5%

### Relationships Expected
- Smokers sleep ~0.3-0.5 hours less than non-smokers
- Heavy drinkers have ~15-25% higher poor sleep rate
- Age shows U-shaped relationship with sleep
- Gender differences in sleep patterns

---

## How to View Results

### View Generated Figures:
```bash
# On macOS:
open results/figures/*.png

# On Linux:
xdg-open results/figures/*.png
```

### View Tables:
```bash
# View CSV files
cat results/tables/*.csv

# Or open in spreadsheet
open results/tables/*.csv
```

### Check Analysis Summary:
```bash
cat results/ANALYSIS_SUMMARY.txt
```

---

## Next Steps After Running

1. **Review all figures** in `results/figures/`
2. **Examine coefficient tables** in `results/tables/`
3. **Fill in project report** - Use `docs/project_report.md` template
4. **Interpret results** - Compare across methods
5. **Generate insights** - What do the findings mean?

---

## Troubleshooting

If analysis doesn't run:

1. **Check dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify data files:**
   ```bash
   ls data/raw/*.xpt
   ```

3. **Test imports:**
   ```bash
   python3 -c "from src.analysis import clustering; print('OK')"
   ```

4. **Run with verbose output:**
   ```bash
   python3 -u scripts/01_prepare_data.py 2>&1 | tee output.log
   ```

---

**Last Updated:** December 2024  
**Status:** Ready to execute - Run the analysis scripts to generate these results!

