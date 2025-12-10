#!/usr/bin/env python3
"""
Run Complete Analysis Pipeline
Executes all analysis steps in sequence
"""

import sys
from pathlib import Path

# Add parent directory to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def run_step(script_name, description):
    """Run an analysis step"""
    print("\n" + "="*80)
    print(f"RUNNING: {description}")
    print("="*80)
    
    script_path = Path(__file__).parent / script_name
    
    if not script_path.exists():
        print(f"Error: {script_path} not found!")
        return False
    
    # Import and run
    import importlib.util
    spec = importlib.util.spec_from_file_location("step", script_path)
    step_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(step_module)
    
    if hasattr(step_module, 'main'):
        step_module.main()
        return True
    else:
        print(f"Error: {script_name} does not have a main() function")
        return False

def main():
    """Run complete analysis pipeline"""
    print("="*80)
    print("COMPLETE ANALYSIS PIPELINE")
    print("Sleep Quality Analysis: Effects of Smoking and Alcohol")
    print("="*80)
    
    steps = [
        ('01_prepare_data.py', 'Data Preparation'),
        ('02_clustering.py', 'K-Means Clustering'),
        ('03_regression.py', 'Linear Regression'),
        ('04_decision_trees.py', 'Decision Trees')
    ]
    
    for script, description in steps:
        success = run_step(script, description)
        if not success:
            print(f"\n✗ Pipeline stopped at: {description}")
            return
    
    print("\n" + "="*80)
    print("✓ ALL ANALYSES COMPLETE!")
    print("="*80)
    print("\nResults are saved in the 'results/' directory:")
    print("  - figures/ : All visualizations")
    print("  - tables/  : Summary tables and coefficients")
    print("  - models/  : Saved model objects (if applicable)")
    print("\nReview the results and see docs/project_report.md for interpretation.")

if __name__ == "__main__":
    main()

