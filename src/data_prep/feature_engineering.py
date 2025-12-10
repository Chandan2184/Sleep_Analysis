"""
Feature Engineering
Functions to create derived variables for analysis
"""

import numpy as np
import pandas as pd


def create_sleep_variables(df):
    """
    Create derived sleep variables
    
    Parameters:
    -----------
    df : DataFrame
        Dataframe with sleep variables
    
    Returns:
    --------
    DataFrame
        Dataframe with additional sleep variables
    """
    df = df.copy()
    
    # Sleep duration difference (weekend - weekday)
    df['SLEEP_DIFF'] = df['SLD013'] - df['SLD012']
    
    # Average sleep hours
    df['AVG_SLEEP'] = (df['SLD012'] + df['SLD013']) / 2
    
    # Poor sleep indicators
    df['POOR_SLEEP_DIAGNOSIS'] = (df['SLQ050'] == 1).astype(int)
    df['LOW_SLEEP_HOURS'] = (df['AVG_SLEEP'] < 6).astype(int)
    df['HIGH_SLEEPINESS'] = (df['SLQ120'] >= 3).astype(int)
    
    # Composite poor sleep indicator
    df['POOR_SLEEP'] = ((df['POOR_SLEEP_DIAGNOSIS'] == 1) | 
                        (df['LOW_SLEEP_HOURS'] == 1) | 
                        (df['HIGH_SLEEPINESS'] == 1)).astype(int)
    
    return df


def create_smoking_variables(df):
    """
    Create derived smoking variables
    
    Parameters:
    -----------
    df : DataFrame
        Dataframe with smoking variables
    
    Returns:
    --------
    DataFrame
        Dataframe with additional smoking variables
    """
    df = df.copy()
    
    # Smoking status (1=Current, 2=Former, 3=Never)
    # SMQ020: Ever smoked 100+ cigarettes (1=Yes, 2=No)
    # SMQ040: Smoke now (1=Every day, 2=Some days, 3=Not at all)
    
    df['SMOKING_STATUS'] = np.nan
    df.loc[df['SMQ020'] == 2, 'SMOKING_STATUS'] = 3  # Never
    df.loc[(df['SMQ020'] == 1) & (df['SMQ040'] == 3), 'SMOKING_STATUS'] = 2  # Former
    df.loc[(df['SMQ020'] == 1) & (df['SMQ040'].isin([1, 2])), 'SMOKING_STATUS'] = 1  # Current
    
    # Current smoker binary
    df['CURRENT_SMOKER'] = (df['SMOKING_STATUS'] == 1).astype(int)
    
    # Cigarettes per day (0 for never/former smokers)
    df['CIGARETTES_PER_DAY'] = df['SMD641'].fillna(0)
    df.loc[df['SMOKING_STATUS'].isin([2, 3]), 'CIGARETTES_PER_DAY'] = 0
    
    return df


def create_alcohol_variables(df):
    """
    Create derived alcohol variables
    
    Parameters:
    -----------
    df : DataFrame
        Dataframe with alcohol variables
    
    Returns:
    --------
    DataFrame
        Dataframe with additional alcohol variables
    """
    df = df.copy()
    
    # Alcohol status categories
    # ALQ130: Average drinks per day (past 12 months)
    # Categories: 0=None, 1=Light (1-2), 2=Moderate (3-4), 3=Heavy (5+)
    
    df['ALCOHOL_STATUS'] = np.nan
    df.loc[df['ALQ111'] == 2, 'ALCOHOL_STATUS'] = 0  # Never
    df.loc[(df['ALQ130'] >= 0.1) & (df['ALQ130'] <= 2), 'ALCOHOL_STATUS'] = 1  # Light
    df.loc[(df['ALQ130'] > 2) & (df['ALQ130'] <= 4), 'ALCOHOL_STATUS'] = 2  # Moderate
    df.loc[df['ALQ130'] > 4, 'ALCOHOL_STATUS'] = 3  # Heavy
    
    # Fill never drinkers
    df.loc[df['ALQ111'] == 2, 'ALCOHOL_STATUS'] = 0
    
    # Average drinks per day (set to 0 for never drinkers)
    df['AVG_DRINKS_DAY'] = df['ALQ130'].fillna(0)
    df.loc[df['ALQ111'] == 2, 'AVG_DRINKS_DAY'] = 0
    
    # Heavy drinker binary
    df['HEAVY_DRINKER'] = (df['ALCOHOL_STATUS'] == 3).astype(int)
    
    # Binge drinker
    df['BINGE_DRINKER'] = (df['ALQ151'] >= 2).astype(int)
    
    return df


def create_demographic_variables(df):
    """
    Create derived demographic variables
    
    Parameters:
    -----------
    df : DataFrame
        Dataframe with demographic variables
    
    Returns:
    --------
    DataFrame
        Dataframe with additional demographic variables
    """
    df = df.copy()
    
    # Age groups
    df['AGE_GROUP'] = pd.cut(df['RIDAGEYR'], 
                            bins=[0, 29, 44, 59, 80], 
                            labels=['18-29', '30-44', '45-59', '60+'])
    
    # Low income indicator (below 130% of poverty line)
    df['LOW_INCOME'] = (df['INDFMPIR'] < 1.3).astype(int)
    
    # Gender (keep as 1=Male, 2=Female)
    df['GENDER'] = df['RIAGENDR']
    
    return df


def select_analysis_variables(df):
    """
    Select variables for analysis
    
    Parameters:
    -----------
    df : DataFrame
        Merged dataframe with all variables
    
    Returns:
    --------
    DataFrame
        Dataframe with selected variables only
    """
    # Core identifiers
    core_vars = ['SEQN']
    
    # Sleep outcomes
    sleep_outcomes = ['SLD012', 'SLD013', 'SLQ030', 'SLQ050', 'SLQ120', 
                     'SLEEP_DIFF', 'AVG_SLEEP', 'POOR_SLEEP', 
                     'POOR_SLEEP_DIAGNOSIS', 'LOW_SLEEP_HOURS', 'HIGH_SLEEPINESS']
    
    # Smoking predictors
    smoking_vars = ['SMQ020', 'SMQ040', 'SMOKING_STATUS', 'CURRENT_SMOKER', 
                   'CIGARETTES_PER_DAY', 'SMD641']
    
    # Alcohol predictors
    alcohol_vars = ['ALQ111', 'ALQ130', 'ALCOHOL_STATUS', 'AVG_DRINKS_DAY', 
                   'HEAVY_DRINKER', 'BINGE_DRINKER', 'ALQ151']
    
    # Demographics/Controls
    demo_vars = ['RIAGENDR', 'RIDAGEYR', 'RIDRETH1', 'DMDEDUC2', 
                'INDFMPIR', 'DMDHHSIZ', 'AGE_GROUP', 'LOW_INCOME', 'GENDER']
    
    # Select variables that exist in dataframe
    all_vars = core_vars + sleep_outcomes + smoking_vars + alcohol_vars + demo_vars
    selected_vars = [v for v in all_vars if v in df.columns]
    
    df_selected = df[selected_vars].copy()
    
    print(f"\nSelected {len(selected_vars)} variables for analysis")
    
    return df_selected

