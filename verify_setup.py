#!/usr/bin/env python3
"""
Verify Project Setup
Checks that all required files and directories are in place
"""

from pathlib import Path
import sys

def check_setup():
    """Verify project setup"""
    project_root = Path(__file__).parent
    
    print("="*80)
    print("VERIFYING PROJECT SETUP")
    print("="*80)
    
    issues = []
    warnings = []
    
    # Check directory structure
    required_dirs = [
        'data/raw',
        'data/processed',
        'src/data_prep',
        'src/analysis',
        'scripts',
        'results/figures',
        'results/tables',
        'docs'
    ]
    
    print("\n1. Checking directory structure...")
    for dir_path in required_dirs:
        full_path = project_root / dir_path
        if full_path.exists():
            print(f"   ✓ {dir_path}")
        else:
            print(f"   ✗ {dir_path} - MISSING")
            issues.append(f"Directory missing: {dir_path}")
    
    # Check required Python files
    required_files = [
        'src/data_prep/load_data.py',
        'src/data_prep/clean_data.py',
        'src/data_prep/feature_engineering.py',
        'src/analysis/clustering.py',
        'src/analysis/regression.py',
        'src/analysis/decision_trees.py',
        'scripts/01_prepare_data.py',
        'scripts/02_clustering.py',
        'scripts/03_regression.py',
        'scripts/04_decision_trees.py',
        'scripts/run_all_analysis.py',
        'requirements.txt',
        'README.md'
    ]
    
    print("\n2. Checking required Python files...")
    for file_path in required_files:
        full_path = project_root / file_path
        if full_path.exists():
            print(f"   ✓ {file_path}")
        else:
            print(f"   ✗ {file_path} - MISSING")
            issues.append(f"File missing: {file_path}")
    
    # Check data files
    print("\n3. Checking data files...")
    data_dir = project_root / 'data' / 'raw'
    required_data = ['ALQ_J.xpt', 'DEMO_J.xpt', 'SLQ_J.xpt', 'SMQ_J.xpt']
    
    if data_dir.exists():
        existing_files = list(data_dir.glob('*.xpt'))
        existing_names = [f.name for f in existing_files]
        
        for data_file in required_data:
            if data_file in existing_names:
                print(f"   ✓ {data_file}")
            else:
                print(f"   ⚠ {data_file} - NOT FOUND (add to data/raw/)")
                warnings.append(f"Data file missing: {data_file}")
    else:
        print("   ✗ data/raw directory does not exist")
        issues.append("data/raw directory missing")
    
    # Check Python packages
    print("\n4. Checking Python packages...")
    required_packages = [
        'pandas', 'numpy', 'sklearn', 'matplotlib', 
        'seaborn', 'pyreadstat', 'statsmodels'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"   ✓ {package}")
        except ImportError:
            print(f"   ✗ {package} - NOT INSTALLED")
            missing_packages.append(package)
    
    if missing_packages:
        warnings.append(f"Install missing packages: pip install {' '.join(missing_packages)}")
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    
    if not issues and not warnings:
        print("✓ All checks passed! Project is ready to use.")
        print("\nNext steps:")
        print("  1. Add .xpt files to data/raw/ (if not already done)")
        print("  2. Run: python scripts/run_all_analysis.py")
        return True
    else:
        if issues:
            print(f"✗ {len(issues)} critical issue(s) found:")
            for issue in issues:
                print(f"  - {issue}")
        
        if warnings:
            print(f"\n⚠ {len(warnings)} warning(s):")
            for warning in warnings:
                print(f"  - {warning}")
        
        print("\nPlease fix the issues above before running the analysis.")
        return False

if __name__ == "__main__":
    success = check_setup()
    sys.exit(0 if success else 1)

