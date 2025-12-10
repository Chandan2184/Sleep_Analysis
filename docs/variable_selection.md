# Quick Reference: Variable Selection Guide

## Variables to Keep for Sleep Analysis with Smoking and Drinking

### ✅ KEEP THESE VARIABLES

---

## 1. SLEEP OUTCOMES (Primary Dependent Variables)

| Variable | File | Description | Keep? |
|----------|------|-------------|-------|
| `SEQN` | All | Respondent ID (for merging) | ✅ **YES** |
| `SLD012` | SLQ_J | Sleep hours - weekdays | ✅ **YES - Primary Outcome** |
| `SLD013` | SLQ_J | Sleep hours - weekends | ✅ **YES - Primary Outcome** |
| `SLQ030` | SLQ_J | Sleep quality rating | ✅ **YES - Primary Outcome** |
| `SLQ050` | SLQ_J | Ever told doctor had trouble sleeping | ✅ **YES - Primary Outcome** |
| `SLQ120` | SLQ_J | Daytime sleepiness frequency | ✅ **YES - Primary Outcome** |
| `SLQ040` | SLQ_J | Sleep apnea symptoms | ✅ **YES - Secondary** |

---

## 2. SMOKING VARIABLES (Primary Predictors)

| Variable | File | Description | Keep? |
|----------|------|-------------|-------|
| `SMQ020` | SMQ_J | Smoked ≥100 cigarettes lifetime | ✅ **YES** |
| `SMQ040` | SMQ_J | Smoke now (1=Every day, 2=Some days, 3=Not at all) | ✅ **YES** |
| `SMD641` | SMQ_J | Cigarettes per day | ✅ **YES** |
| `SMD030` | SMQ_J | Age started smoking | ✅ **YES - Optional** |

**Create Derived:**
- `SMOKING_STATUS` (Never/Former/Current)
- `CURRENT_SMOKER` (Binary)
- `CIGARETTES_PER_DAY` (Numeric, 0 for non-smokers)

---

## 3. ALCOHOL VARIABLES (Primary Predictors)

| Variable | File | Description | Keep? |
|----------|------|-------------|-------|
| `ALQ111` | ALQ_J | Ever had a drink | ✅ **YES** |
| `ALQ130` | ALQ_J | Avg drinks/day - past 12 months | ✅ **YES - Primary** |
| `ALQ142` | ALQ_J | Number of days drank alcohol | ✅ **YES - Optional** |
| `ALQ151` | ALQ_J | Binge drinking frequency | ✅ **YES - Optional** |
| `ALQ170` | ALQ_J | Heavy drinking days | ✅ **YES - Optional** |

**Create Derived:**
- `ALCOHOL_STATUS` (Never/Light/Moderate/Heavy)
- `AVG_DRINKS_DAY` (Numeric)
- `HEAVY_DRINKER` (Binary)
- `BINGE_DRINKER` (Binary)

---

## 4. DEMOGRAPHIC/CONTROL VARIABLES

| Variable | File | Description | Keep? |
|----------|------|-------------|-------|
| `RIAGENDR` | DEMO_J | Gender (1=Male, 2=Female) | ✅ **YES - Control** |
| `RIDAGEYR` | DEMO_J | Age in years | ✅ **YES - Control** |
| `RIDRETH1` | DEMO_J | Race/Hispanic origin | ✅ **YES - Control** |
| `INDFMPIR` | DEMO_J | Poverty income ratio | ✅ **YES - Control** |
| `DMDEDUC2` | DEMO_J | Education level | ✅ **YES - Control** |
| `DMDHHSIZ` | DEMO_J | Household size | ✅ **Optional** |
| `DMDMARTL` | DEMO_J | Marital status | ✅ **Optional** |

**Create Derived:**
- `AGE_GROUP` (Categorical)
- `LOW_INCOME` (Binary)

---

## 5. OPTIONAL: ADDITIONAL CONTROLS

| Variable | File | Description | Keep? |
|----------|------|-------------|-------|
| `DPQ030` | DPQ_J | Trouble sleeping (from PHQ-9) | ⚠️ **Use with caution** (circular) |
| `DPQ_TOTAL` | DPQ_J | Total depression score | ✅ **Optional - Control** |
| `BPQ020` | BPQ_J | High blood pressure | ✅ **Optional - Control** |

---

## ❌ DO NOT KEEP THESE VARIABLES

| Variable | File | Reason to Exclude |
|----------|------|-------------------|
| `SLQ300`, `SLQ310`, `SLQ320`, `SLQ330` | SLQ_J | Use calculated SLD012/SLD013 instead |
| `SMDUPCA`, `SMD100BR` | SMQ_J | Cigarette brand names (not relevant) |
| `SDDSRVYR` | DEMO_J | All same value (2017-2018) |
| Variables with >50% missing | All | Too much missing data |
| Most variables from BPQ_J | BPQ_J | Not relevant to sleep-smoking-alcohol analysis |

---

## Variable Usage by Analysis Type

### For K-Means Clustering:
- `SMOKING_STATUS` (encoded)
- `ALCOHOL_STATUS` (encoded)
- `RIDAGEYR` (standardized)
- `RIAGENDR` (encoded)
- `INDFMPIR` (standardized)
- `CIGARETTES_PER_DAY` (standardized)
- `AVG_DRINKS_DAY` (standardized)

### For Linear Regression (Predictors):
- All smoking variables
- All alcohol variables
- All demographic controls
- Interaction terms: `SMOKING_STATUS × ALCOHOL_STATUS`

### For Linear Regression (Outcomes):
- `SLD012` (continuous)
- `SLD013` (continuous)
- `SLQ030` (continuous/ordinal)
- `SLQ120` (continuous/ordinal)

### For Decision Trees (Features):
- All predictors listed above
- All demographic controls

### For Decision Trees (Target):
- `POOR_SLEEP` (binary classification)
- `SLD012` (regression)

---

## Minimum Variable Set (Core Analysis)

If you need to minimize variables, keep these **essential** ones:

**Outcomes:**
- `SLD012`, `SLQ030`, `SLQ050`, `POOR_SLEEP`

**Predictors:**
- `SMOKING_STATUS`, `CIGARETTES_PER_DAY`
- `ALCOHOL_STATUS`, `AVG_DRINKS_DAY`
- `RIDAGEYR`, `RIAGENDR`, `INDFMPIR`

**Total: 10 variables** (plus SEQN for merging)

---

## Data Quality Notes

### High Quality (Keep):
- Sleep variables: <1% missing
- Core demographics: 0% missing
- `SMQ020`: 12.9% missing
- `ALQ111`: 7.3% missing

### Moderate Quality (Use with caution):
- `ALQ130`: 36.8% missing (expected - only drinkers answer)
- `SMQ040`: 64.8% missing (expected - only smokers answer)
- `SMD641`: 84.2% missing (expected - only current smokers)

### Missing Data Strategy:
1. **Listwise deletion** for primary analysis
2. **Create indicator variables** for missing smoking/alcohol (separate category)
3. **Multiple imputation** for sensitivity analysis

---

## Quick Checklist

Before starting analysis, ensure you have:

- [ ] Merged all datasets on `SEQN`
- [ ] Created all derived variables (SMOKING_STATUS, ALCOHOL_STATUS, etc.)
- [ ] Cleaned special values (7, 9, 77, 99 → NaN)
- [ ] Created outcome variables (POOR_SLEEP, AVG_SLEEP, etc.)
- [ ] Handled missing data appropriately
- [ ] Standardized variables for clustering
- [ ] Created interaction terms for regression

---

*This guide provides the essential variables needed for the sleep-smoking-alcohol analysis project.*

