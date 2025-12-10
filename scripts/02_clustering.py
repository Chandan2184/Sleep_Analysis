#!/usr/bin/env python3
"""
Step 2: K-Means Clustering Analysis
Identify lifestyle clusters based on smoking, alcohol, and demographics
"""

import sys
from pathlib import Path

# Add parent directory to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'src'))

import pandas as pd
from analysis.clustering import perform_kmeans_clustering

def main():
    """Main clustering analysis"""
    print("="*80)
    print("STEP 2: K-MEANS CLUSTERING ANALYSIS")
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
    
    # Perform clustering
    results = perform_kmeans_clustering(df, n_clusters=4, output_dir=str(output_dir))
    
    print("\n✓ Clustering analysis complete!")
    print(f"Results saved to: {output_dir}")
    
    return results

if __name__ == "__main__":
    results = main()

