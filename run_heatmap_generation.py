#!/usr/bin/env python3
"""
Simple Heatmap Runner
"""

import sys
import pandas as pd
from pathlib import Path

# Add src and scripts to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / 'src'))
sys.path.insert(0, str(project_root / 'scripts'))

print("="*80)
print("CORRELATION HEATMAP - RUNNING NOW")
print("="*80)

# Load data
data_file = project_root / 'data' / 'processed' / 'prepared_sleep_analysis_data.csv'
if not data_file.exists():
    print(f"Error: Data file not found at {data_file}")
    print("Please run the data preparation script first (e.g., 'scripts/01_prepare_data.py')")
    sys.exit(1)

print(f"\n[1/2] Loading data from: {data_file}")
df = pd.read_csv(data_file)
print(f"✓ Loaded {len(df):,} rows, {len(df.columns)} columns")

# Ensure results directories
results_dir = project_root / 'results' / 'figures'
results_dir.mkdir(parents=True, exist_ok=True)

# Run heatmap generation
print("\n" + "="*80)
print("[2/2] GENERATING HEATMAP")
print("="*80)

try:
    from scripts.a5_generate_correlation_heatmap import generate_heatmap
    generate_heatmap(df, results_dir)
    print("✓ Heatmap generation complete - results saved")
except Exception as e:
    print(f"✗ Heatmap error: {e}")

print("\n" + "="*80)
print("HEATMAP GENERATION COMPLETE!")
print("="*80)
print(f"\nAll results saved in: {results_dir}")
