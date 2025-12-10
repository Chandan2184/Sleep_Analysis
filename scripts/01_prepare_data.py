#!/usr/bin/env python3
"""
Step 1: Data Preparation
Load, clean, and prepare NHANES data for analysis
"""

import sys
from pathlib import Path

# Add parent directory to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'src'))

import pandas as pd
import numpy as np
from data_prep import (
    load_nhanes_data, merge_datasets, clean_special_values,
    create_sleep_variables, create_smoking_variables,
    create_alcohol_variables, create_demographic_variables
)
from data_prep.feature_engineering import select_analysis_variables

def main():
    """Main data preparation pipeline"""
    print("="*80)
    print("STEP 1: DATA PREPARATION")
    print("="*80)
    
    # Set paths
    data_dir = project_root / 'data' / 'raw'
    output_dir = project_root / 'data' / 'processed'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Load data
    demo, slq, alq, smq, dpq = load_nhanes_data(data_dir)
    
    # Clean special values
    print("\nCleaning special values...")
    demo = clean_special_values(demo)
    slq = clean_special_values(slq)
    alq = clean_special_values(alq)
    smq = clean_special_values(smq)
    dpq = clean_special_values(dpq)
    
    # Create derived variables
    print("\nCreating derived variables...")
    slq = create_sleep_variables(slq)
    smq = create_smoking_variables(smq)
    alq = create_alcohol_variables(alq)
    demo = create_demographic_variables(demo)
    
    # Merge datasets
    merged = merge_datasets(demo, slq, alq, smq, dpq)
    
    # Clean merged dataset
    merged = clean_special_values(merged)
    
    # Select variables for analysis
    final_df = select_analysis_variables(merged)
    
    # Save prepared dataset
    output_file = output_dir / 'prepared_sleep_analysis_data.csv'
    final_df.to_csv(output_file, index=False)
    print(f"\n✓ Prepared dataset saved to: {output_file}")
    
    # Summary statistics
    print("\n" + "="*80)
    print("DATASET SUMMARY")
    print("="*80)
    print(f"Total rows: {len(final_df):,}")
    print(f"Total columns: {len(final_df.columns)}")
    print(f"\nMissing data summary:")
    missing_pct = (final_df.isnull().sum() / len(final_df) * 100).sort_values(ascending=False)
    print(missing_pct[missing_pct > 0].head(10))
    
    print("\n" + "="*80)
    print("KEY VARIABLE SUMMARY")
    print("="*80)
    key_vars = ['SLD012', 'SLD013', 'SLQ030', 'SLQ120', 'POOR_SLEEP',
               'SMOKING_STATUS', 'CURRENT_SMOKER', 'CIGARETTES_PER_DAY',
               'ALCOHOL_STATUS', 'AVG_DRINKS_DAY', 'HEAVY_DRINKER',
               'RIDAGEYR', 'RIAGENDR']
    
    available_key_vars = [v for v in key_vars if v in final_df.columns]
    print(final_df[available_key_vars].describe())
    
    print("\n✓ Data preparation complete!")
    return final_df

if __name__ == "__main__":
    df = main()

