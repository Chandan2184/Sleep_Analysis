"""
Load NHANES Data Files
Functions to load and merge NHANES datasets
"""

import pyreadstat
from pathlib import Path


def load_nhanes_data(data_dir):
    """
    Load all NHANES data files from directory
    
    Parameters:
    -----------
    data_dir : str or Path
        Directory containing NHANES .xpt files
    
    Returns:
    --------
    tuple : (demo, slq, alq, smq, dpq)
        DataFrames for demographics, sleep, alcohol, smoking, and depression
    """
    print("Loading NHANES data files...")
    
    data_dir = Path(data_dir)
    
    # Load each dataset
    demo, _ = pyreadstat.read_xport(data_dir / "DEMO_J.xpt")
    slq, _ = pyreadstat.read_xport(data_dir / "SLQ_J.xpt")
    alq, _ = pyreadstat.read_xport(data_dir / "ALQ_J.xpt")
    smq, _ = pyreadstat.read_xport(data_dir / "SMQ_J.xpt")
    dpq, _ = pyreadstat.read_xport(data_dir / "DPQ_J.xpt")
    
    print(f"Loaded datasets:")
    print(f"  DEMO: {len(demo)} rows")
    print(f"  SLQ:  {len(slq)} rows")
    print(f"  ALQ:  {len(alq)} rows")
    print(f"  SMQ:  {len(smq)} rows")
    print(f"  DPQ:  {len(dpq)} rows")
    
    return demo, slq, alq, smq, dpq


def merge_datasets(demo, slq, alq, smq, dpq=None):
    """
    Merge all datasets on SEQN (respondent sequence number)
    
    Parameters:
    -----------
    demo : DataFrame
        Demographics data
    slq : DataFrame
        Sleep questionnaire data
    alq : DataFrame
        Alcohol questionnaire data
    smq : DataFrame
        Smoking questionnaire data
    dpq : DataFrame, optional
        Depression questionnaire data
    
    Returns:
    --------
    DataFrame
        Merged dataset
    """
    print("\nMerging datasets...")
    
    # Start with demographics (largest dataset)
    merged = demo.copy()
    
    # Merge sleep
    merged = merged.merge(slq, on='SEQN', how='inner', suffixes=('', '_slq'))
    
    # Merge alcohol
    merged = merged.merge(alq, on='SEQN', how='inner', suffixes=('', '_alq'))
    
    # Merge smoking
    merged = merged.merge(smq, on='SEQN', how='inner', suffixes=('', '_smq'))
    
    # Optionally merge depression
    if dpq is not None:
        merged = merged.merge(dpq, on='SEQN', how='inner', suffixes=('', '_dpq'))
    
    print(f"Merged dataset: {len(merged)} rows, {len(merged.columns)} columns")
    
    return merged

