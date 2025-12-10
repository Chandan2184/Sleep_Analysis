#!/usr/bin/env python3
"""
Step 5: Generate Correlation Heatmap
"""

import sys
from pathlib import Path
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Add parent directory to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'src'))

def generate_heatmap(df, output_dir):
    """Generates and saves a correlation heatmap."""
    
    # Select only numeric columns for correlation
    numeric_df = df.select_dtypes(include=['number'])
    
    # Calculate correlation matrix
    corr = numeric_df.corr()

    # Generate and save heatmap
    plt.figure(figsize=(20, 16))
    sns.heatmap(corr, annot=False, cmap='viridis', linewidths=.5)
    plt.title('Correlation Heatmap of Numeric Variables', fontsize=18)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    
    output_file = output_dir / 'correlation_heatmap.png'
    plt.savefig(output_file, dpi=300)
    print(f"\n✓ Correlation heatmap saved to: {output_file}")

def main():
    """Main function to generate correlation heatmap"""
    print("="*80)
    print("STEP 5: GENERATE CORRELATION HEATMAP")
    print("="*80)

    # Set paths
    project_root = Path(__file__).resolve().parent.parent
    data_dir = project_root / 'data' / 'processed'
    output_dir = project_root / 'results' / 'figures'
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load data
    data_file = data_dir / 'prepared_sleep_analysis_data.csv'
    if not data_file.exists():
        print(f"Error: Data file not found at {data_file}")
        print("Please run the data preparation script first (e.g., 'scripts/01_prepare_data.py')")
        sys.exit(1)
        
    df = pd.read_csv(data_file)
    print(f"✓ Data loaded from {data_file}")

    generate_heatmap(df, output_dir)

if __name__ == "__main__":
    main()
