#!/usr/bin/env python3
"""
Simplified Analysis Runner
Runs the complete analysis pipeline with better error handling
"""

import sys
import traceback
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / 'src'))

print("="*80)
print("SLEEP QUALITY ANALYSIS - COMPLETE PIPELINE")
print("="*80)

# Step 1: Data Preparation
print("\n" + "="*80)
print("STEP 1: DATA PREPARATION")
print("="*80)

try:
    from scripts import prepare_data
    print("Importing from scripts module...")
except:
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("step1", project_root / "scripts" / "01_prepare_data.py")
        step1 = importlib.util.module_from_spec(spec)
        sys.path.insert(0, str(project_root))
        spec.loader.exec_module(step1)
        if hasattr(step1, 'main'):
            df = step1.main()
            print("✓ Step 1 completed successfully")
        else:
            print("✗ Step 1 script missing main() function")
    except Exception as e:
        print(f"✗ Error in Step 1: {e}")
        traceback.print_exc()
        sys.exit(1)

# Check if data file was created
data_file = project_root / 'data' / 'processed' / 'prepared_sleep_analysis_data.csv'
if data_file.exists():
    print(f"✓ Prepared data file exists: {data_file}")
else:
    print(f"✗ Prepared data file not found: {data_file}")
    sys.exit(1)

# Step 2: Clustering
print("\n" + "="*80)
print("STEP 2: K-MEANS CLUSTERING")
print("="*80)

try:
    import importlib.util
    spec = importlib.util.spec_from_file_location("step2", project_root / "scripts" / "02_clustering.py")
    step2 = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(project_root))
    spec.loader.exec_module(step2)
    if hasattr(step2, 'main'):
        step2.main()
        print("✓ Step 2 completed successfully")
    else:
        print("✗ Step 2 script missing main() function")
except Exception as e:
    print(f"✗ Error in Step 2: {e}")
    traceback.print_exc()

# Step 3: Regression
print("\n" + "="*80)
print("STEP 3: LINEAR REGRESSION")
print("="*80)

try:
    spec = importlib.util.spec_from_file_location("step3", project_root / "scripts" / "03_regression.py")
    step3 = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(project_root))
    spec.loader.exec_module(step3)
    if hasattr(step3, 'main'):
        step3.main()
        print("✓ Step 3 completed successfully")
    else:
        print("✗ Step 3 script missing main() function")
except Exception as e:
    print(f"✗ Error in Step 3: {e}")
    traceback.print_exc()

# Step 4: Decision Trees
print("\n" + "="*80)
print("STEP 4: DECISION TREES")
print("="*80)

try:
    spec = importlib.util.spec_from_file_location("step4", project_root / "scripts" / "04_decision_trees.py")
    step4 = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(project_root))
    spec.loader.exec_module(step4)
    if hasattr(step4, 'main'):
        step4.main()
        print("✓ Step 4 completed successfully")
    else:
        print("✗ Step 4 script missing main() function")
except Exception as e:
    print(f"✗ Error in Step 4: {e}")
    traceback.print_exc()

print("\n" + "="*80)
print("ANALYSIS COMPLETE!")
print("="*80)
print(f"\nResults saved in: {project_root / 'results'}")
print(f"  - Figures: results/figures/")
print(f"  - Tables: results/tables/")

