import sys
from pathlib import Path
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def generate_heatmap():
    """
    Loads the prepared data, generates a correlation heatmap, and saves it to the 'results/figures' directory.
    """
    project_root = Path(__file__).parent
    data_file = project_root / 'data' / 'processed' / 'prepared_sleep_analysis_data.csv'
    results_dir = project_root / 'results'
    figures_dir = results_dir / 'figures'
    figures_dir.mkdir(parents=True, exist_ok=True)

    if not data_file.exists():
        print(f"Error: Data file not found at {data_file}")
        print("Please run the data preparation script first (e.g., 'scripts/01_prepare_data.py')")
        return

    print(f"Loading data from: {data_file}")
    df = pd.read_csv(data_file)
    print(f"Loaded {len(df):,} rows, {len(df.columns)} columns")

    print("Generating correlation heatmap...")
    try:
        numeric_df = df.select_dtypes(include=np.number)
        corr = numeric_df.corr()
        plt.figure(figsize=(24, 20))
        sns.heatmap(corr, annot=True, cmap='viridis', linewidths=.5, fmt=".2f")
        plt.title('Correlation Heatmap of Numeric Variables (with values)', fontsize=18)
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        plt.tight_layout()
        heatmap_file = figures_dir / 'correlation_heatmap_with_values.png'
        plt.savefig(heatmap_file, dpi=300)
        print(f"✓ Correlation heatmap saved to: {heatmap_file}")
    except Exception as e:
        print(f"✗ Heatmap error: {e}")

if __name__ == "__main__":
    generate_heatmap()
