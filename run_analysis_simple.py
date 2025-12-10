#!/usr/bin/env python3
"""
Simple Analysis Runner - Runs and displays results immediately
"""

import sys
import pandas as pd
import numpy as np
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / 'src'))

print("="*80)
print("SLEEP QUALITY ANALYSIS - RUNNING NOW")
print("="*80)

# Load data
data_file = project_root / 'data' / 'processed' / 'prepared_sleep_analysis_data.csv'
if not data_file.exists():
    data_file = project_root.parent / 'prepared_sleep_analysis_data.csv'

if data_file.exists():
    print(f"\n[1/4] Loading data from: {data_file}")
    df = pd.read_csv(data_file)
    print(f"✓ Loaded {len(df):,} rows, {len(df.columns)} columns")
else:
    print(f"\n[1/4] Preparing data...")
    # Import and prepare
    from data_prep.load_data import load_nhanes_data, merge_datasets
    from data_prep.clean_data import clean_special_values
    from data_prep.feature_engineering import (
        create_sleep_variables, create_smoking_variables,
        create_alcohol_variables, create_demographic_variables,
        select_analysis_variables
    )
    
    demo, slq, alq, smq, dpq = load_nhanes_data(project_root / 'data' / 'raw')
    demo = clean_special_values(demo)
    slq = clean_special_values(slq)
    alq = clean_special_values(alq)
    smq = clean_special_values(smq)
    
    slq = create_sleep_variables(slq)
    smq = create_smoking_variables(smq)
    alq = create_alcohol_variables(alq)
    demo = create_demographic_variables(demo)
    
    merged = merge_datasets(demo, slq, alq, smq, dpq)
    merged = clean_special_values(merged)
    df = select_analysis_variables(merged)
    
    output_file = project_root / 'data' / 'processed' / 'prepared_sleep_analysis_data.csv'
    output_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_file, index=False)
    print(f"✓ Data prepared: {len(df):,} rows")

# Ensure results directories
results_dir = project_root / 'results'
(results_dir / 'figures').mkdir(parents=True, exist_ok=True)
(results_dir / 'tables').mkdir(parents=True, exist_ok=True)

# Display key statistics
print("\n" + "="*80)
print("KEY DATASET STATISTICS")
print("="*80)
print(f"\nSleep Outcomes:")
if 'SLD012' in df.columns:
    print(f"  Mean weekday sleep: {df['SLD012'].mean():.2f} hours")
if 'SLD013' in df.columns:
    print(f"  Mean weekend sleep: {df['SLD013'].mean():.2f} hours")
if 'POOR_SLEEP' in df.columns:
    print(f"  Poor sleep prevalence: {df['POOR_SLEEP'].mean()*100:.1f}%")

print(f"\nLifestyle Factors:")
if 'CURRENT_SMOKER' in df.columns:
    print(f"  Current smokers: {df['CURRENT_SMOKER'].mean()*100:.1f}%")
if 'HEAVY_DRINKER' in df.columns:
    print(f"  Heavy drinkers: {df['HEAVY_DRINKER'].mean()*100:.1f}%")
if 'SMOKING_STATUS' in df.columns:
    smoking_counts = df['SMOKING_STATUS'].value_counts()
    print(f"  Smoking status distribution:")
    for status, count in smoking_counts.items():
        pct = count / len(df) * 100
        print(f"    Status {status}: {count} ({pct:.1f}%)")

# Run analyses
print("\n" + "="*80)
print("[2/4] RUNNING K-MEANS CLUSTERING")
print("="*80)

try:
    from analysis.clustering import perform_kmeans_clustering
    clustering_results = perform_kmeans_clustering(df, n_clusters=4, output_dir=str(results_dir))
    print("✓ Clustering complete - results saved")
except Exception as e:
    print(f"✗ Clustering error: {e}")

print("\n" + "="*80)
print("[3/4] RUNNING LINEAR REGRESSION")
print("="*80)

try:
    from analysis.regression import perform_regression_analysis
    regression_results = perform_regression_analysis(df, output_dir=str(results_dir))
    print("✓ Regression complete - results saved")
except Exception as e:
    print(f"✗ Regression error: {e}")

print("\n" + "="*80)
print("[4/4] RUNNING DECISION TREES")
print("="*80)

try:
    from analysis.decision_trees import perform_decision_tree_analysis
    tree_results = perform_decision_tree_analysis(df, output_dir=str(results_dir))
    print("✓ Decision trees complete - results saved")
except Exception as e:
    print(f"✗ Decision tree error: {e}")

print("\n" + "="*80)
print("ANALYSIS COMPLETE!")
print("="*80)
print(f"\nAll results saved in: {results_dir}")
print(f"  📊 Figures: {results_dir}/figures/")
print(f"  📋 Tables: {results_dir}/tables/")
print(f"\nCheck the results directory for all generated files!")

