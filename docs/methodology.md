# Project Proposal: Sleep Quality Analysis Using Smoking and Alcohol Consumption Patterns

## Project Overview
**Title:** Predicting Sleep Quality Through Lifestyle Factors: A Machine Learning Approach to Understanding Smoking and Alcohol Effects on Sleep Patterns

**Objective:** Analyze how smoking and alcohol consumption patterns affect sleep quality using unsupervised learning (K-means clustering), supervised learning (linear regression and decision trees), and identify lifestyle clusters that predict poor sleep outcomes.

---

## 1. Variable Selection

### 1.1 Primary Outcome Variables (Sleep - from SLQ_J.xpt)
**Keep these variables as dependent variables:**

| Variable | Description | Usage | Missing % |
|----------|-------------|-------|-----------|
| `SEQN` | Respondent ID (for merging) | Key | 0% |
| `SLD012` | Sleep hours on weekdays/workdays | **Primary outcome** | <1% |
| `SLD013` | Sleep hours on weekends | Secondary outcome | <1% |
| `SLQ030` | Sleep quality rating | **Primary outcome** | 0% |
| `SLQ050` | Ever told doctor had trouble sleeping (1=Yes, 2=No) | **Primary outcome** | 0% |
| `SLQ120` | Daytime sleepiness frequency (0-9 scale) | **Primary outcome** | 0% |
| `SLQ040` | Sleep apnea symptoms | Secondary predictor | 0% |

**Derived Variables to Create:**
- `SLEEP_DIFF`: Difference between weekend and weekday sleep (SLD013 - SLD012)
- `POOR_SLEEP`: Binary indicator (1 if SLQ050=1 OR SLQ030 ≥ threshold OR SLQ120 ≥ threshold)
- `AVG_SLEEP`: Average of weekday and weekend sleep hours

---

### 1.2 Primary Predictor Variables

#### A. Alcohol Variables (from ALQ_J.xpt)
**Keep these variables:**

| Variable | Description | Usage | Missing % |
|----------|-------------|-------|-----------|
| `ALQ111` | Ever had a drink (1=Yes, 2=No) | **Primary predictor** | 7.3% |
| `ALQ130` | Avg drinks/day past 12 months | **Primary predictor** | 36.8% |
| `ALQ142` | Number of days drank alcohol | Secondary predictor | 36.8% |
| `ALQ151` | Binge drinking frequency | Secondary predictor | 17.9% |
| `ALQ170` | Heavy drinking days | Secondary predictor | 37.0% |

**Derived Variables to Create:**
- `ALCOHOL_STATUS`: Categorical (Never, Light, Moderate, Heavy) based on ALQ130
- `BINGE_DRINKER`: Binary (1 if ALQ151 indicates frequent binge drinking)
- `HEAVY_DRINKER`: Binary (1 if ALQ170 > 0)

**Coding Notes:**
- ALQ130: Values > 10 may be codes (check NHANES docs)
- Typical coding: 1-10 = actual drinks, 77=Refused, 99=Don't know

---

#### B. Smoking Variables (from SMQ_J.xpt)
**Keep these variables:**

| Variable | Description | Usage | Missing % |
|----------|-------------|-------|-----------|
| `SMQ020` | Smoked ≥100 cigarettes lifetime (1=Yes, 2=No) | **Primary predictor** | 12.9% |
| `SMQ040` | Smoke now (1=Every day, 2=Some days, 3=Not at all) | **Primary predictor** | 64.8% |
| `SMD030` | Age started smoking regularly | Secondary predictor | 64.9% |
| `SMD641` | Cigarettes per day (current smokers) | **Primary predictor** | 84.2% |
| `SMD650` | Years since quit (former smokers) | Secondary predictor | 84.8% |
| `SMQ050Q` | Days smoked in past 30 days | Secondary predictor | 80.0% |

**Derived Variables to Create:**
- `SMOKING_STATUS`: Categorical (Never, Former, Current Light, Current Heavy)
- `PACK_YEARS`: Estimated pack-years (if age and duration available)
- `CURRENT_SMOKER`: Binary (1 if SMQ040 = 1 or 2)
- `CIGARETTES_PER_DAY`: Numeric (0 for never/former, SMD641 for current)

**Coding Notes:**
- SMQ040: Only asked if SMQ020=1
- Missing values are expected (only smokers answer detailed questions)

---

### 1.3 Control/Covariate Variables (from DEMO_J.xpt)
**Keep these variables:**

| Variable | Description | Usage | Missing % |
|----------|-------------|-------|-----------|
| `RIAGENDR` | Gender (1=Male, 2=Female) | **Control** | 0% |
| `RIDAGEYR` | Age in years | **Control** | 0% |
| `RIDRETH1` | Race/Hispanic origin | **Control** | 0% |
| `DMDEDUC2` | Education level (adults 20+) | **Control** | 39.8% |
| `DMDMARTL` | Marital status | Control | 39.8% |
| `INDFMPIR` | Poverty income ratio | **Control** | 13.3% |
| `DMDHHSIZ` | Household size | Control | 0% |
| `WTINT2YR` | Survey weight | For weighted analysis | 0% |

**Derived Variables to Create:**
- `AGE_GROUP`: Categorical (18-29, 30-44, 45-59, 60+)
- `LOW_INCOME`: Binary (1 if INDFMPIR < 1.3)

---

### 1.4 Additional Control Variables (Optional but Recommended)

#### From DPQ_J.xpt (Depression - affects sleep):
- `DPQ030`: Trouble falling/staying asleep (from PHQ-9)
- `DPQ_TOTAL`: Sum of all DPQ variables (depression score)
- **Note:** DPQ030 is specifically about sleep, but use cautiously to avoid circularity

#### From BPQ_J.xpt (Health conditions - may affect sleep):
- `BPQ020`: Ever told had high blood pressure
- Could indicate health-related sleep issues

---

### 1.5 Variables to EXCLUDE
- `SLQ300`, `SLQ310`, `SLQ320`, `SLQ330`: Time strings (use calculated SLD012, SLD013 instead)
- `SMDUPCA`, `SMD100BR`: Cigarette brand names (not relevant)
- `SDDSRVYR`: Survey year (all same value)
- Most missing variables (>50% missing) unless critically important
- Variables with codes 7, 9, 77, 99 (refused/don't know) - recode as missing

---

## 2. Project Methodology: K-Means, Linear Regression, and Decision Trees

### 2.1 Project Structure

```
Project: Sleep Quality Prediction
├── Phase 1: Data Preparation & Exploration
├── Phase 2: K-Means Clustering (Unsupervised)
├── Phase 3: Linear Regression (Supervised)
├── Phase 4: Decision Trees (Supervised)
└── Phase 5: Integration & Insights
```

---

### 2.2 Phase 1: Data Preparation

**Tasks:**
1. **Data Merging:**
   - Merge DEMO_J, SLQ_J, ALQ_J, SMQ_J using `SEQN`
   - Handle different sample sizes (inner join recommended)
   - Final dataset: ~5,000-6,000 participants with complete data

2. **Data Cleaning:**
   - Recode special values (7, 9, 77, 99, 777, 999) as NaN
   - Handle missing data:
     - Listwise deletion for primary analysis
     - Multiple imputation for sensitivity analysis
   - Create derived variables (see above)

3. **Feature Engineering:**
   - Create interaction terms: `SMOKING × ALCOHOL`
   - Create composite scores
   - Standardize continuous variables for clustering

4. **Exploratory Data Analysis:**
   - Descriptive statistics
   - Correlation matrices
   - Visualizations (boxplots, histograms, scatter plots)

---

### 2.3 Phase 2: K-Means Clustering

**Objective:** Identify distinct lifestyle clusters based on smoking, alcohol, and demographic patterns.

**Method:**
1. **Variables for Clustering:**
   - `SMOKING_STATUS` (encoded)
   - `ALCOHOL_STATUS` (encoded)
   - `RIDAGEYR` (standardized)
   - `RIAGENDR` (encoded)
   - `INDFMPIR` (standardized)
   - `CIGARETTES_PER_DAY` (standardized)
   - `ALQ130` (avg drinks/day, standardized)

2. **Process:**
   - Determine optimal k using elbow method and silhouette analysis
   - Run K-means with k=3, 4, 5, 6 clusters
   - Analyze cluster characteristics
   - Validate clusters using sleep outcomes

3. **Expected Clusters:**
   - **Cluster 1:** Healthy lifestyle (non-smokers, light/no alcohol)
   - **Cluster 2:** Moderate risk (occasional smoking/drinking)
   - **Cluster 3:** High risk (heavy smoking and/or heavy drinking)
   - **Cluster 4:** Former users (quit smoking/drinking)
   - Additional clusters may emerge based on demographics

4. **Analysis:**
   - Compare mean sleep quality across clusters
   - Test for significant differences (ANOVA)
   - Visualize clusters in 2D/3D space (PCA)

**Deliverable:** Identified lifestyle clusters with distinct sleep patterns

---

### 2.4 Phase 3: Linear Regression

**Objective:** Quantify the relationship between smoking, alcohol, and sleep outcomes.

**Models to Build:**

#### Model 1: Sleep Duration (Continuous Outcome)
```
SLD012 ~ β₀ + β₁(SMOKING_STATUS) + β₂(ALCOHOL_STATUS) + 
         β₃(AGE) + β₄(GENDER) + β₅(INCOME) + 
         β₆(SMOKING × ALCOHOL) + ε
```

#### Model 2: Sleep Quality (Continuous/Ordinal Outcome)
```
SLQ030 ~ β₀ + β₁(SMOKING_STATUS) + β₂(ALCOHOL_STATUS) + 
         β₃(CIGARETTES_PER_DAY) + β₄(ALQ130) + 
         β₅(AGE) + β₆(GENDER) + β₇(INCOME) + ε
```

#### Model 3: Daytime Sleepiness
```
SLQ120 ~ β₀ + β₁(SMOKING_STATUS) + β₂(ALCOHOL_STATUS) + 
         β₃(SLD012) + β₄(AGE) + β₅(GENDER) + ε
```

**Process:**
1. Check assumptions (linearity, homoscedasticity, normality)
2. Handle multicollinearity (VIF scores)
3. Model selection (backward/forward stepwise)
4. Model diagnostics (residual plots, leverage)
5. Interpret coefficients with confidence intervals

**Expected Insights:**
- Quantify how many hours of sleep are lost per pack/day
- Quantify effect of heavy drinking on sleep quality
- Test for interaction effects

---

### 2.5 Phase 4: Decision Trees

**Objective:** Identify key predictors and decision rules for poor sleep outcomes.

**Models to Build:**

#### Model 1: Classification Tree
**Target:** `POOR_SLEEP` (binary: 1=poor sleep, 0=good sleep)

**Features:**
- Smoking variables
- Alcohol variables
- Demographics
- Health indicators

**Process:**
1. Train/test split (70/30)
2. Build decision tree with max_depth tuning
3. Prune tree to avoid overfitting
4. Visualize tree structure
5. Extract decision rules

#### Model 2: Regression Tree
**Target:** `SLD012` (sleep hours - continuous)

**Features:** Same as above

#### Model 3: Random Forest (Optional Extension)
- Ensemble of decision trees
- Feature importance ranking
- More robust predictions

**Deliverables:**
- Visual decision tree showing key splits
- Feature importance rankings
- Decision rules (e.g., "If smokes >20 cigarettes/day AND drinks >3/day, then poor sleep probability = 85%")

---

### 2.6 Phase 5: Integration & Comparison

**Tasks:**
1. **Compare Methods:**
   - How do clusters from K-means relate to decision tree splits?
   - Do linear regression coefficients align with decision tree importance?
   - Which method provides best predictions?

2. **Synthesize Findings:**
   - Create comprehensive profile of high-risk groups
   - Identify actionable insights
   - Create recommendations

3. **Validation:**
   - Cross-validation for regression and trees
   - Cluster stability analysis
   - Sensitivity analysis with different variable selections

---

## 3. Research Questions That Can Be Answered

### 3.1 Primary Research Questions

#### Q1: How does smoking status affect sleep quality and duration?
- **Approach:** Compare sleep outcomes across smoking status (never, former, current)
- **Methods:** ANOVA, Linear regression, Decision trees
- **Expected Answer:** Current smokers sleep X hours less and have Y% higher probability of poor sleep

#### Q2: How does alcohol consumption affect sleep patterns?
- **Approach:** Compare sleep outcomes across alcohol consumption levels
- **Methods:** Linear regression with alcohol as continuous/categorical predictor
- **Expected Answer:** Heavy drinkers (>3 drinks/day) have X hours less sleep and Y points lower sleep quality

#### Q3: Is there an interaction effect between smoking and alcohol on sleep?
- **Approach:** Include interaction term in regression: SMOKING × ALCOHOL
- **Methods:** Linear regression with interaction terms
- **Expected Answer:** Combined heavy smoking and drinking has multiplicative negative effect on sleep

#### Q4: What lifestyle clusters exist in the population, and how do they differ in sleep outcomes?
- **Approach:** K-means clustering on lifestyle variables
- **Methods:** K-means clustering, cluster comparison
- **Expected Answer:** Identify 4-6 distinct clusters with significantly different sleep patterns

#### Q5: Which factors are most important in predicting poor sleep quality?
- **Approach:** Feature importance from decision trees
- **Methods:** Decision trees, Random forest
- **Expected Answer:** Rank order: Smoking status > Alcohol > Age > Gender > Income

#### Q6: What are the decision rules for identifying individuals at risk for poor sleep?
- **Approach:** Extract rules from decision tree
- **Methods:** Decision tree visualization and rule extraction
- **Expected Answer:** "If smokes >10 cigarettes/day OR drinks >4/day OR age >65, then high risk"

---

### 3.2 Secondary Research Questions

#### Q7: Does the effect of smoking/alcohol on sleep differ by age or gender?
- **Approach:** Stratified analysis or interaction terms
- **Expected Answer:** Effects stronger in older adults, or gender-specific patterns

#### Q8: How does weekend vs. weekday sleep differ by lifestyle factors?
- **Approach:** Compare SLD012 vs. SLD013 across groups
- **Expected Answer:** Smokers/drinkers show larger weekend sleep "catch-up"

#### Q9: Do former smokers/drinkers have better sleep than current users?
- **Approach:** Compare never, former, current groups
- **Expected Answer:** Former users have intermediate sleep quality between never and current

#### Q10: What is the combined population-attributable risk of smoking and alcohol on poor sleep?
- **Approach:** Calculate PAF using regression coefficients
- **Expected Answer:** X% of poor sleep cases attributable to smoking/alcohol

---

### 3.3 Exploratory Questions

#### Q11: Are there demographic differences in smoking/alcohol effects on sleep?
- **Approach:** Stratified regression by race, income, education
- **Expected Answer:** Effects may vary by socioeconomic status

#### Q12: Can we predict sleep quality accurately enough for screening purposes?
- **Approach:** Evaluate model performance (AUC, accuracy, sensitivity)
- **Expected Answer:** Decision tree achieves X% accuracy, suitable/not suitable for screening

#### Q13: What is the dose-response relationship between alcohol consumption and sleep?
- **Approach:** Non-linear regression or splines
- **Expected Answer:** Curvilinear relationship (light drinking may have minimal effect, heavy has strong effect)

#### Q14: How does binge drinking pattern affect sleep differently than regular moderate drinking?
- **Approach:** Compare ALQ151 (binge frequency) vs. ALQ130 (regular consumption)
- **Expected Answer:** Binge drinking may have different/additional effects

---

## 4. Expected Outcomes & Deliverables

### 4.1 Analytical Deliverables
1. **Cleaned, merged dataset** with all selected variables
2. **Cluster profiles** from K-means analysis (3-6 clusters with characteristics)
3. **Regression models** with coefficients, p-values, R² values
4. **Decision tree(s)** with visualizations and rules
5. **Feature importance rankings** from multiple methods
6. **Model comparison** (performance metrics: RMSE, MAE, accuracy, AUC)

### 4.2 Insights & Findings
1. **Quantified effects:** "Smoking 1 pack/day reduces sleep by X hours"
2. **Risk profiles:** Identification of high-risk groups
3. **Decision rules:** Actionable criteria for identifying at-risk individuals
4. **Interaction effects:** How smoking and alcohol interact
5. **Population estimates:** Prevalence of poor sleep attributable to lifestyle factors

### 4.3 Visualizations
1. Cluster visualizations (2D/3D plots)
2. Regression coefficient plots with confidence intervals
3. Decision tree diagrams
4. Feature importance bar charts
5. Sleep outcome distributions by lifestyle groups
6. Interaction effect plots

---

## 5. Technical Implementation Plan

### 5.1 Required Python Libraries
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor, plot_tree
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, r2_score, mean_squared_error
from scipy import stats
import warnings
warnings.filterwarnings('ignore')
```

### 5.2 Analysis Pipeline
1. Data loading and merging
2. Data cleaning and feature engineering
3. Descriptive statistics and EDA
4. K-means clustering (with optimal k selection)
5. Linear regression (multiple models)
6. Decision trees (classification and regression)
7. Model comparison and validation
8. Results synthesis and visualization

---

## 6. Limitations & Considerations

1. **Missing Data:** Significant missingness in some variables requires careful handling
2. **Causal Inference:** Cross-sectional data limits causal conclusions (association only)
3. **Self-Report Bias:** Sleep, smoking, and alcohol data are self-reported
4. **Survey Design:** Complex survey weights needed for population estimates
5. **Confounding:** Other factors (medications, health conditions) may confound relationships
6. **Sample Size:** After merging, final sample may be reduced to ~5,000-6,000

---

## 7. Timeline & Milestones

- **Week 1:** Data preparation, cleaning, merging
- **Week 2:** K-means clustering and cluster analysis
- **Week 3:** Linear regression modeling
- **Week 4:** Decision tree analysis
- **Week 5:** Integration, validation, and report writing

---

## 8. Success Criteria

✅ Successfully identify 3-6 meaningful lifestyle clusters  
✅ Build regression models explaining ≥15% variance in sleep outcomes  
✅ Achieve decision tree accuracy ≥70% for poor sleep classification  
✅ Identify at least 3 significant predictors of sleep quality  
✅ Quantify effects of smoking and alcohol on sleep with confidence intervals  
✅ Generate actionable insights and recommendations  

---

*This project combines unsupervised learning (clustering), supervised learning (regression and classification), and provides both statistical inference and predictive modeling capabilities.*

