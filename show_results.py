#!/usr/bin/env python3
"""
Show Analysis Results
Computes and displays results from the prepared dataset
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Load data
project_root = Path(__file__).parent
data_file = project_root / 'data' / 'processed' / 'prepared_sleep_analysis_data.csv'
if not data_file.exists():
    data_file = project_root.parent / 'prepared_sleep_analysis_data.csv'

print("="*80)
print("SLEEP QUALITY ANALYSIS - RESULTS")
print("="*80)

df = pd.read_csv(data_file)
print(f"\nDataset: {len(df):,} participants, {len(df.columns)} variables")

# Key Statistics
print("\n" + "="*80)
print("KEY STATISTICS")
print("="*80)

print("\n📊 SLEEP OUTCOMES:")
print("-"*80)
if 'SLD012' in df.columns:
    valid = df['SLD012'].notna()
    print(f"  Weekday Sleep Hours: {df.loc[valid, 'SLD012'].mean():.2f} hours (SD={df.loc[valid, 'SLD012'].std():.2f}, n={valid.sum()})")
if 'SLD013' in df.columns:
    valid = df['SLD013'].notna()
    print(f"  Weekend Sleep Hours: {df.loc[valid, 'SLD013'].mean():.2f} hours (SD={df.loc[valid, 'SLD013'].std():.2f}, n={valid.sum()})")
if 'SLQ030' in df.columns:
    valid = df['SLQ030'].notna()
    print(f"  Sleep Quality (SLQ030): {df.loc[valid, 'SLQ030'].mean():.2f} (SD={df.loc[valid, 'SLQ030'].std():.2f}, n={valid.sum()})")
if 'POOR_SLEEP' in df.columns:
    print(f"  Poor Sleep Prevalence: {df['POOR_SLEEP'].mean()*100:.1f}%")
if 'POOR_SLEEP_DIAGNOSIS' in df.columns:
    print(f"  Sleep Disorder Diagnosis: {df['POOR_SLEEP_DIAGNOSIS'].mean()*100:.1f}%")

print("\n🚬 SMOKING PATTERNS:")
print("-"*80)
if 'SMOKING_STATUS' in df.columns:
    status_counts = df['SMOKING_STATUS'].value_counts().sort_index()
    total = df['SMOKING_STATUS'].notna().sum()
    print(f"  Never Smokers: {status_counts.get(3, 0)} ({status_counts.get(3, 0)/total*100:.1f}%)")
    print(f"  Former Smokers: {status_counts.get(2, 0)} ({status_counts.get(2, 0)/total*100:.1f}%)")
    print(f"  Current Smokers: {status_counts.get(1, 0)} ({status_counts.get(1, 0)/total*100:.1f}%)")
if 'CURRENT_SMOKER' in df.columns:
    print(f"  Current Smoker Rate: {df['CURRENT_SMOKER'].mean()*100:.1f}%")
if 'CIGARETTES_PER_DAY' in df.columns:
    smokers = df[df['CURRENT_SMOKER'] == 1]
    if len(smokers) > 0:
        valid = smokers['CIGARETTES_PER_DAY'].notna()
        if valid.sum() > 0:
            print(f"  Avg Cigarettes/Day (smokers): {smokers.loc[valid, 'CIGARETTES_PER_DAY'].mean():.1f}")

print("\n🍷 ALCOHOL PATTERNS:")
print("-"*80)
if 'ALCOHOL_STATUS' in df.columns:
    status_counts = df['ALCOHOL_STATUS'].value_counts().sort_index()
    total = df['ALCOHOL_STATUS'].notna().sum()
    print(f"  Never Drinkers: {status_counts.get(0, 0)} ({status_counts.get(0, 0)/total*100:.1f}%)")
    print(f"  Light Drinkers: {status_counts.get(1, 0)} ({status_counts.get(1, 0)/total*100:.1f}%)")
    print(f"  Moderate Drinkers: {status_counts.get(2, 0)} ({status_counts.get(2, 0)/total*100:.1f}%)")
    print(f"  Heavy Drinkers: {status_counts.get(3, 0)} ({status_counts.get(3, 0)/total*100:.1f}%)")
if 'HEAVY_DRINKER' in df.columns:
    print(f"  Heavy Drinker Rate: {df['HEAVY_DRINKER'].mean()*100:.1f}%")
if 'AVG_DRINKS_DAY' in df.columns:
    drinkers = df[df['AVG_DRINKS_DAY'] > 0]
    if len(drinkers) > 0:
        print(f"  Avg Drinks/Day (drinkers): {drinkers['AVG_DRINKS_DAY'].mean():.2f}")

print("\n👥 DEMOGRAPHICS:")
print("-"*80)
if 'RIDAGEYR' in df.columns:
    print(f"  Mean Age: {df['RIDAGEYR'].mean():.1f} years (range: {df['RIDAGEYR'].min():.0f}-{df['RIDAGEYR'].max():.0f})")
if 'RIAGENDR' in df.columns:
    gender_counts = df['RIAGENDR'].value_counts()
    total = len(df)
    print(f"  Male: {gender_counts.get(1, 0)} ({gender_counts.get(1, 0)/total*100:.1f}%)")
    print(f"  Female: {gender_counts.get(2, 0)} ({gender_counts.get(2, 0)/total*100:.1f}%)")

# Relationships
print("\n" + "="*80)
print("KEY RELATIONSHIPS")
print("="*80)

if 'SLD012' in df.columns and 'CURRENT_SMOKER' in df.columns:
    print("\n📈 Sleep Duration by Smoking Status:")
    print("-"*80)
    non_smokers = df[df['CURRENT_SMOKER'] == 0]
    smokers = df[df['CURRENT_SMOKER'] == 1]
    if len(non_smokers) > 0 and len(smokers) > 0:
        non_smoker_sleep = non_smokers['SLD012'].mean()
        smoker_sleep = smokers['SLD012'].mean()
        diff = non_smoker_sleep - smoker_sleep
        print(f"  Non-smokers: {non_smoker_sleep:.2f} hours")
        print(f"  Smokers: {smoker_sleep:.2f} hours")
        print(f"  Difference: {diff:.2f} hours ({'smokers sleep less' if diff > 0 else 'smokers sleep more'})")

if 'SLD012' in df.columns and 'HEAVY_DRINKER' in df.columns:
    print("\n📈 Sleep Duration by Drinking Status:")
    print("-"*80)
    non_drinkers = df[df['HEAVY_DRINKER'] == 0]
    heavy_drinkers = df[df['HEAVY_DRINKER'] == 1]
    if len(non_drinkers) > 0 and len(heavy_drinkers) > 0:
        non_drinker_sleep = non_drinkers['SLD012'].mean()
        heavy_drinker_sleep = heavy_drinkers['SLD012'].mean()
        diff = non_drinker_sleep - heavy_drinker_sleep
        print(f"  Non-heavy drinkers: {non_drinker_sleep:.2f} hours")
        print(f"  Heavy drinkers: {heavy_drinker_sleep:.2f} hours")
        print(f"  Difference: {diff:.2f} hours")

if 'POOR_SLEEP' in df.columns and 'CURRENT_SMOKER' in df.columns:
    print("\n📈 Poor Sleep by Smoking Status:")
    print("-"*80)
    non_smokers_ps = df[df['CURRENT_SMOKER'] == 0]['POOR_SLEEP'].mean() * 100
    smokers_ps = df[df['CURRENT_SMOKER'] == 1]['POOR_SLEEP'].mean() * 100
    print(f"  Non-smokers: {non_smokers_ps:.1f}%")
    print(f"  Smokers: {smokers_ps:.1f}%")
    print(f"  Difference: {abs(smokers_ps - non_smokers_ps):.1f} percentage points")

if 'POOR_SLEEP' in df.columns and 'HEAVY_DRINKER' in df.columns:
    print("\n📈 Poor Sleep by Drinking Status:")
    print("-"*80)
    non_drinkers_ps = df[df['HEAVY_DRINKER'] == 0]['POOR_SLEEP'].mean() * 100
    heavy_drinkers_ps = df[df['HEAVY_DRINKER'] == 1]['POOR_SLEEP'].mean() * 100
    print(f"  Non-heavy drinkers: {non_drinkers_ps:.1f}%")
    print(f"  Heavy drinkers: {heavy_drinkers_ps:.1f}%")
    print(f"  Difference: {abs(heavy_drinkers_ps - non_drinkers_ps):.1f} percentage points")

print("\n" + "="*80)
print("ANALYSIS READY TO RUN")
print("="*80)
print("\nTo generate full analysis with visualizations:")
print("  python3 scripts/run_all_analysis.py")
print("\nResults will be saved in:")
print("  - results/figures/  (visualizations)")
print("  - results/tables/   (summary tables)")

