"""
Data Cleaning Functions
Functions to clean and preprocess NHANES data
"""

import numpy as np
import pandas as pd


def clean_special_values(df, columns=None):
    """
    Recode special NHANES values (7, 9, 77, 99, 777, 999) as NaN
    These values typically represent "Refused", "Don't know", or "Not applicable"
    
    Parameters:
    -----------
    df : DataFrame
        Input dataframe
    columns : list, optional
        Specific columns to clean. If None, cleans all numeric columns.
    
    Returns:
    --------
    DataFrame
        Dataframe with special values recoded as NaN
    """
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns
    
    special_values = [7, 9, 77, 99, 777, 999, 7.0, 9.0, 77.0, 99.0, 777.0, 999.0]
    
    for col in columns:
        if col in df.columns:
            df[col] = df[col].replace(special_values, np.nan)
    
    return df


def handle_missing_data(df, strategy='listwise', missing_threshold=0.5):
    """
    Handle missing data using specified strategy
    
    Parameters:
    -----------
    df : DataFrame
        Input dataframe
    strategy : str
        'listwise' - Remove rows with any missing values
        'drop_high_missing' - Remove columns with >threshold missing
    missing_threshold : float
        Threshold for dropping columns (0-1)
    
    Returns:
    --------
    DataFrame
        Cleaned dataframe
    """
    df = df.copy()
    
    if strategy == 'drop_high_missing':
        missing_pct = df.isnull().sum() / len(df)
        cols_to_drop = missing_pct[missing_pct > missing_threshold].index
        df = df.drop(columns=cols_to_drop)
        print(f"Dropped {len(cols_to_drop)} columns with >{missing_threshold*100}% missing")
    
    elif strategy == 'listwise':
        initial_rows = len(df)
        df = df.dropna()
        dropped_rows = initial_rows - len(df)
        print(f"Listwise deletion: Dropped {dropped_rows} rows ({dropped_rows/initial_rows*100:.1f}%)")
    
    return df

