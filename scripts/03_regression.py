#!/usr/bin/env python3
"""
Step 3: Linear Regression Analysis
Quantify relationships between smoking, alcohol, and sleep outcomes
"""

import sys
from pathlib import Path

# Add parent directory to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'src'))

import pandas as pd
from analysis.regression import perform_regression_analysis

def main():
    """Main regression analysis"""
    print("="*80)
    print("STEP 3: LINEAR REGRESSION ANALYSIS")
    print("="*80)
    
    # Load prepared data
    data_file = project_root / 'data' / 'processed' / 'prepared_sleep_analysis_data.csv'
    
    if not data_file.exists():
        print(f"Error: {data_file} not found. Please run 01_prepare_data.py first.")
        return
    
    df = pd.read_csv(data_file)
    print(f"Loaded data: {len(df)} rows, {len(df.columns)} columns")
    
    # Set output directory
    output_dir = project_root / 'results'
    
    # Perform regression analysis
    results = perform_regression_analysis(df, output_dir=str(output_dir))
    
    print("\n✓ Regression analysis complete!")
    print(f"Results saved to: {output_dir}")
    
    return results

if __name__ == "__main__":
    results = main()

