# Project Report: Sleep Quality Analysis

## Effects of Smoking and Alcohol Consumption on Sleep Patterns

## Executive Summary

This project investigates the relationships between lifestyle factors (smoking and alcohol consumption) and sleep quality using data from the National Health and Nutrition Examination Survey (NHANES) 2017-2018. Three machine learning approaches were employed:

1. **K-Means Clustering** - Identified distinct lifestyle groups
2. **Linear Regression** - Quantified relationships between predictors and sleep outcomes
3. **Decision Trees** - Identified key predictors and decision rules

**Key Findings:**
- [Insert key findings from your analysis]
- [Insert quantitative results]
- [Insert actionable insights]

---

## 1. Introduction

### 1.1 Background

Sleep quality is a critical component of overall health and well-being. Lifestyle factors such as smoking and alcohol consumption have been shown to affect sleep patterns, but the complex interactions between these factors are not fully understood.

### 1.2 Research Questions

1. How does smoking status affect sleep quality and duration?
2. How does alcohol consumption affect sleep patterns?
3. Is there an interaction effect between smoking and alcohol on sleep?
4. What lifestyle clusters exist in the population, and how do they differ in sleep outcomes?
5. Which factors are most important in predicting poor sleep quality?
6. What are the decision rules for identifying individuals at risk for poor sleep?

### 1.3 Dataset

**NHANES 2017-2018 (Cycle J)**
- **Sample Size:** 5,533 participants with complete data
- **Variables:** 34 selected variables covering sleep, smoking, alcohol, and demographics
- **Data Sources:**
  - DEMO_J: Demographics
  - SLQ_J: Sleep questionnaire
  - ALQ_J: Alcohol questionnaire
  - SMQ_J: Smoking questionnaire
  - DPQ_J: Depression questionnaire (used as control)

---

## 2. Methodology

### 2.1 Data Preparation

**Steps:**
1. Loaded and merged datasets on `SEQN` (respondent ID)
2. Recoded special values (7, 9, 77, 99, 777, 999) as missing
3. Created derived variables:
   - Smoking status (Never/Former/Current)
   - Alcohol status (Never/Light/Moderate/Heavy)
   - Poor sleep indicators
   - Age groups, income indicators
4. Selected 34 variables for analysis
5. Handled missing data using listwise deletion for complete-case analysis

**Final Dataset:**
- 5,533 participants
- Complete cases vary by analysis (due to missing data patterns)

### 2.2 K-Means Clustering

**Objective:** Identify lifestyle clusters based on smoking, alcohol, and demographics

**Method:**
- Features: SMOKING_STATUS, ALCOHOL_STATUS, Age, Gender, Income, Cigarettes/Day, Drinks/Day
- Standardized all features
- Tested k=2 to k=8 using elbow method and silhouette analysis
- Selected optimal k based on silhouette score
- Analyzed cluster characteristics and sleep outcomes by cluster

**Evaluation:**
- Silhouette scores
- Cluster size distribution
- Sleep outcome comparisons across clusters

### 2.3 Linear Regression

**Objective:** Quantify relationships between predictors and sleep outcomes

**Models:**
1. **Model 1:** Sleep Duration (SLD012) ~ Smoking + Alcohol + Demographics
2. **Model 2:** Sleep Quality (SLQ030) ~ Smoking + Alcohol + Demographics
3. **Model 3:** Daytime Sleepiness (SLQ120) ~ Smoking + Alcohol + Sleep Hours + Demographics

**Method:**
- Ordinary Least Squares (OLS) regression
- Checked assumptions (linearity, homoscedasticity, normality of residuals)
- Reported coefficients, p-values, confidence intervals, R²

**Evaluation Metrics:**
- R² (coefficient of determination)
- RMSE (Root Mean Squared Error)
- Coefficient significance (p < 0.05)

### 2.4 Decision Trees

**Objective:** Identify key predictors and decision rules

**Models:**
1. **Classification Tree:** Predict Poor Sleep (binary)
2. **Regression Tree:** Predict Sleep Duration (continuous)
3. **Random Forest:** Ensemble method for comparison

**Method:**
- Train/test split (70/30)
- Tuned max_depth, min_samples_split, min_samples_leaf
- Extracted feature importance
- Visualized tree structure
- Generated decision rules

**Evaluation Metrics:**
- Classification: Accuracy, Precision, Recall, F1-score
- Regression: R², RMSE

---

## 3. Results

### 3.1 Descriptive Statistics

[Include key descriptive statistics from your analysis]

**Sleep Outcomes:**
- Mean weekday sleep: X hours
- Mean weekend sleep: Y hours
- Poor sleep prevalence: Z%

**Lifestyle Factors:**
- Current smokers: X%
- Heavy drinkers: Y%
- Combined heavy smoking and drinking: Z%

### 3.2 K-Means Clustering Results

[Describe your clustering results]

**Identified Clusters:**
1. **Cluster 1:** [Description - e.g., Healthy lifestyle]
2. **Cluster 2:** [Description]
3. **Cluster 3:** [Description]
4. **Cluster 4:** [Description]

**Sleep Outcomes by Cluster:**
- Cluster X has lowest sleep duration (Y hours)
- Cluster Z has highest poor sleep rate (W%)

### 3.3 Linear Regression Results

[Present your regression results]

**Model 1: Sleep Duration**
- Significant predictors: [List]
- Smoking effect: Current smokers sleep X hours less than non-smokers (β = -X, p < 0.05)
- Alcohol effect: Heavy drinkers sleep Y hours less (β = -Y, p < 0.05)
- R² = X.XX

**Model 2: Sleep Quality**
[Similar format]

**Model 3: Daytime Sleepiness**
[Similar format]

### 3.4 Decision Tree Results

[Present your decision tree results]

**Key Predictors (Ranked by Importance):**
1. [Variable] - Importance: X.XX
2. [Variable] - Importance: Y.YY
3. [Variable] - Importance: Z.ZZ

**Decision Rules:**
- If [condition], then [outcome]
- Example: "If smokes >10 cigarettes/day OR drinks >4/day, then 85% probability of poor sleep"

**Model Performance:**
- Classification Accuracy: X%
- Regression R²: Y.YY

---

## 4. Discussion

### 4.1 Key Findings

[Discuss your main findings]

### 4.2 Interpretation

[Interpret what the results mean]

### 4.3 Comparison of Methods

**K-Means Clustering:**
- Strengths: Identified natural groupings, no assumptions about relationships
- Limitations: Requires interpretation, no direct prediction

**Linear Regression:**
- Strengths: Quantifies relationships, provides confidence intervals
- Limitations: Assumes linearity, may miss complex interactions

**Decision Trees:**
- Strengths: Easy to interpret, captures non-linear relationships
- Limitations: Can overfit, less stable than ensemble methods

### 4.4 Limitations

1. **Cross-sectional Data:** Cannot establish causation, only associations
2. **Missing Data:** Listwise deletion may introduce bias
3. **Self-Reported Measures:** Potential recall and social desirability bias
4. **Confounding:** Unmeasured factors may affect relationships
5. **Survey Weights:** Not used in this analysis (affects generalizability)

### 4.5 Future Work

1. Use survey weights for population-level estimates
2. Multiple imputation for missing data
3. Explore interaction effects more deeply
4. Add other lifestyle factors (exercise, diet)
5. Longitudinal analysis if data available

---

## 5. Conclusions

[Summarize main conclusions]

**Main Takeaways:**
1. [Key finding 1]
2. [Key finding 2]
3. [Key finding 3]

**Practical Implications:**
- Public health interventions should target [group]
- Healthcare providers should screen for [factors]
- Future research should investigate [areas]

---

## 6. References

1. NHANES Data Documentation. Centers for Disease Control and Prevention.
2. [Add relevant literature citations]
3. [Add methodology references]

---

## Appendices

### Appendix A: Variable Definitions
[Include variable definitions and coding]

### Appendix B: Additional Figures
[Include supplementary visualizations]

### Appendix C: Model Details
[Include detailed model outputs, diagnostics]

---

**Word Count:** [Approximately X,XXX words]  
**Figures:** X  
**Tables:** Y

