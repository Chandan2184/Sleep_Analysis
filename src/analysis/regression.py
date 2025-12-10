"""
Linear Regression Analysis
Quantify relationships between smoking, alcohol, and sleep outcomes
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import statsmodels.api as sm
import joblib


def perform_regression_analysis(df, output_dir='results'):
    """
    Perform linear regression analysis on sleep outcomes
    
    Parameters:
    -----------
    df : DataFrame
        Input dataframe
    output_dir : str
        Directory to save results
    
    Returns:
    --------
    dict
        Regression results for all models
    """
    print("\n" + "="*80)
    print("LINEAR REGRESSION ANALYSIS")
    print("="*80)
    
    results = {}
    
    # Prepare data
    regression_vars = [
        'SMOKING_STATUS', 'ALCOHOL_STATUS', 'CIGARETTES_PER_DAY', 
        'AVG_DRINKS_DAY', 'RIDAGEYR', 'RIAGENDR', 'INDFMPIR',
        'SLD012', 'SLQ030', 'SLQ120'
    ]
    
    df_reg = df[regression_vars].dropna()
    print(f"\nComplete cases for regression: {len(df_reg)}")
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    (output_path / 'figures').mkdir(exist_ok=True)
    (output_path / 'tables').mkdir(exist_ok=True)
    (output_path / 'models').mkdir(exist_ok=True)
    
    # Model 1: Sleep Duration (SLD012)
    print("\n" + "-"*80)
    print("MODEL 1: Sleep Duration (SLD012)")
    print("-"*80)
    
    X1 = df_reg[['SMOKING_STATUS', 'ALCOHOL_STATUS', 'CIGARETTES_PER_DAY', 
                 'AVG_DRINKS_DAY', 'RIDAGEYR', 'RIAGENDR', 'INDFMPIR']]
    y1 = df_reg['SLD012']
    
    # Add constant for statsmodels
    X1_sm = sm.add_constant(X1)
    model1_sm = sm.OLS(y1, X1_sm).fit()
    
    print(model1_sm.summary())
    
    # Predictions
    y1_pred = model1_sm.predict(X1_sm)
    r2_1 = r2_score(y1, y1_pred)
    rmse_1 = np.sqrt(mean_squared_error(y1, y1_pred))
    
    print(f"\nR² = {r2_1:.4f}")
    print(f"RMSE = {rmse_1:.4f}")
    
    # Save coefficients
    coeffs1 = pd.DataFrame({
        'Variable': model1_sm.params.index,
        'Coefficient': model1_sm.params.values,
        'P-value': model1_sm.pvalues.values,
        'Std Error': model1_sm.bse.values
    })
    coeffs1.to_csv(f'{output_dir}/tables/regression_model1_coefficients.csv', index=False)
    
    model1_path = output_path / 'models' / 'regression_model1_sleep_duration.joblib'
    joblib.dump(model1_sm, model1_path)
    results['model1'] = {
        'model': model1_sm,
        'r2': r2_1,
        'rmse': rmse_1,
        'coefficients': coeffs1
    }
    
    # Model 2: Sleep Quality (SLQ030)
    print("\n" + "-"*80)
    print("MODEL 2: Sleep Quality (SLQ030)")
    print("-"*80)
    
    X2 = df_reg[['SMOKING_STATUS', 'ALCOHOL_STATUS', 'CIGARETTES_PER_DAY', 
                 'AVG_DRINKS_DAY', 'RIDAGEYR', 'RIAGENDR', 'INDFMPIR']]
    y2 = df_reg['SLQ030']
    
    X2_sm = sm.add_constant(X2)
    model2_sm = sm.OLS(y2, X2_sm).fit()
    
    print(model2_sm.summary())
    
    y2_pred = model2_sm.predict(X2_sm)
    r2_2 = r2_score(y2, y2_pred)
    rmse_2 = np.sqrt(mean_squared_error(y2, y2_pred))
    
    print(f"\nR² = {r2_2:.4f}")
    print(f"RMSE = {rmse_2:.4f}")
    
    coeffs2 = pd.DataFrame({
        'Variable': model2_sm.params.index,
        'Coefficient': model2_sm.params.values,
        'P-value': model2_sm.pvalues.values,
        'Std Error': model2_sm.bse.values
    })
    coeffs2.to_csv(f'{output_dir}/tables/regression_model2_coefficients.csv', index=False)
    
    model2_path = output_path / 'models' / 'regression_model2_sleep_quality.joblib'
    joblib.dump(model2_sm, model2_path)
    results['model2'] = {
        'model': model2_sm,
        'r2': r2_2,
        'rmse': rmse_2,
        'coefficients': coeffs2
    }
    
    # Model 3: Daytime Sleepiness (SLQ120)
    print("\n" + "-"*80)
    print("MODEL 3: Daytime Sleepiness (SLQ120)")
    print("-"*80)
    
    X3 = df_reg[['SMOKING_STATUS', 'ALCOHOL_STATUS', 'CIGARETTES_PER_DAY', 
                 'AVG_DRINKS_DAY', 'SLD012', 'RIDAGEYR', 'RIAGENDR']]
    y3 = df_reg['SLQ120']
    
    X3_sm = sm.add_constant(X3)
    model3_sm = sm.OLS(y3, X3_sm).fit()
    
    print(model3_sm.summary())
    
    y3_pred = model3_sm.predict(X3_sm)
    r2_3 = r2_score(y3, y3_pred)
    rmse_3 = np.sqrt(mean_squared_error(y3, y3_pred))
    
    print(f"\nR² = {r2_3:.4f}")
    print(f"RMSE = {rmse_3:.4f}")
    
    coeffs3 = pd.DataFrame({
        'Variable': model3_sm.params.index,
        'Coefficient': model3_sm.params.values,
        'P-value': model3_sm.pvalues.values,
        'Std Error': model3_sm.bse.values
    })
    coeffs3.to_csv(f'{output_dir}/tables/regression_model3_coefficients.csv', index=False)
    
    model3_path = output_path / 'models' / 'regression_model3_daytime_sleepiness.joblib'
    joblib.dump(model3_sm, model3_path)
    results['model3'] = {
        'model': model3_sm,
        'r2': r2_3,
        'rmse': rmse_3,
        'coefficients': coeffs3
    }
    
    # Visualization: Coefficient plots
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    for idx, (model_key, ax) in enumerate(zip(['model1', 'model2', 'model3'], axes)):
        coeffs = results[model_key]['coefficients']
        # Exclude constant
        coeffs_plot = coeffs[coeffs['Variable'] != 'const'].copy()
        coeffs_plot = coeffs_plot.sort_values('Coefficient')
        
        colors = ['red' if p < 0.05 else 'gray' for p in coeffs_plot['P-value']]
        ax.barh(coeffs_plot['Variable'], coeffs_plot['Coefficient'], color=colors)
        ax.axvline(x=0, color='black', linestyle='--', linewidth=0.5)
        ax.set_xlabel('Coefficient')
        ax.set_title(f'Model {idx+1} Coefficients')
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/figures/regression_coefficients.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Residual plots
    fig, axes = plt.subplots(3, 2, figsize=(14, 12))
    
    models = [model1_sm, model2_sm, model3_sm]
    outcomes = [y1, y2, y3]
    model_names = ['Sleep Duration', 'Sleep Quality', 'Daytime Sleepiness']
    
    for idx, (model, y, name) in enumerate(zip(models, outcomes, model_names)):
        # Predicted vs Actual
        y_pred = model.fittedvalues
        axes[idx, 0].scatter(y_pred, y, alpha=0.5)
        axes[idx, 0].plot([y.min(), y.max()], [y.min(), y.max()], 'r--', lw=2)
        axes[idx, 0].set_xlabel('Predicted')
        axes[idx, 0].set_ylabel('Actual')
        axes[idx, 0].set_title(f'{name} - Predicted vs Actual')
        axes[idx, 0].grid(True, alpha=0.3)
        
        # Residuals
        residuals = y - y_pred
        axes[idx, 1].scatter(y_pred, residuals, alpha=0.5)
        axes[idx, 1].axhline(y=0, color='r', linestyle='--', lw=2)
        axes[idx, 1].set_xlabel('Predicted')
        axes[idx, 1].set_ylabel('Residuals')
        axes[idx, 1].set_title(f'{name} - Residual Plot')
        axes[idx, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/figures/regression_diagnostics.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return results
