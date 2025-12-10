"""
Decision Tree Analysis
Identify key predictors and decision rules for sleep outcomes
"""

import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor, plot_tree
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import (accuracy_score, classification_report, confusion_matrix,
                            r2_score, mean_squared_error)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import joblib


def perform_decision_tree_analysis(df, output_dir='results'):
    """
    Perform decision tree analysis
    
    Parameters:
    -----------
    df : DataFrame
        Input dataframe
    output_dir : str
        Directory to save results
    
    Returns:
    --------
    dict
        Decision tree results
    """
    print("\n" + "="*80)
    print("DECISION TREE ANALYSIS")
    print("="*80)
    
    results = {}
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    (output_path / 'figures').mkdir(exist_ok=True)
    (output_path / 'tables').mkdir(exist_ok=True)
    (output_path / 'models').mkdir(exist_ok=True)
    
    # Prepare features
    feature_cols = [
        'SMOKING_STATUS', 'ALCOHOL_STATUS', 'CIGARETTES_PER_DAY', 
        'AVG_DRINKS_DAY', 'RIDAGEYR', 'RIAGENDR', 'INDFMPIR'
    ]
    
    # Model 1: Classification Tree - Poor Sleep
    print("\n" + "-"*80)
    print("MODEL 1: Classification Tree - Poor Sleep (Binary)")
    print("-"*80)
    
    df_class = df[feature_cols + ['POOR_SLEEP']].dropna()
    print(f"Complete cases for classification: {len(df_class)}")
    
    X_class = df_class[feature_cols]
    y_class = df_class['POOR_SLEEP']
    
    # Split data
    X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(
        X_class, y_class, test_size=0.3, random_state=42, stratify=y_class
    )
    
    # Decision Tree
    dt_classifier = DecisionTreeClassifier(max_depth=5, min_samples_split=50, 
                                          min_samples_leaf=50, random_state=42)
    dt_classifier.fit(X_train_c, y_train_c)
    
    y_pred_train = dt_classifier.predict(X_train_c)
    y_pred_test = dt_classifier.predict(X_test_c)
    
    train_accuracy = accuracy_score(y_train_c, y_pred_train)
    test_accuracy = accuracy_score(y_test_c, y_pred_test)
    
    print(f"Training Accuracy: {train_accuracy:.4f}")
    print(f"Test Accuracy: {test_accuracy:.4f}")
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'Feature': feature_cols,
        'Importance': dt_classifier.feature_importances_
    }).sort_values('Importance', ascending=False)
    
    print("\nFeature Importance:")
    print(feature_importance)
    
    # Classification report
    print("\nClassification Report (Test Set):")
    print(classification_report(y_test_c, y_pred_test))
    
    # Random Forest for comparison
    rf_classifier = RandomForestClassifier(n_estimators=100, max_depth=5, 
                                          min_samples_split=50, random_state=42)
    rf_classifier.fit(X_train_c, y_train_c)
    rf_pred_test = rf_classifier.predict(X_test_c)
    rf_accuracy = accuracy_score(y_test_c, rf_pred_test)
    
    print(f"\nRandom Forest Test Accuracy: {rf_accuracy:.4f}")
    
    dt_class_path = output_path / 'models' / 'decision_tree_classifier_poor_sleep.joblib'
    rf_class_path = output_path / 'models' / 'random_forest_classifier_poor_sleep.joblib'
    joblib.dump(dt_classifier, dt_class_path)
    joblib.dump(rf_classifier, rf_class_path)

    results['classification'] = {
        'dt_model': dt_classifier,
        'rf_model': rf_classifier,
        'train_accuracy': train_accuracy,
        'test_accuracy': test_accuracy,
        'rf_accuracy': rf_accuracy,
        'feature_importance': feature_importance
    }
    
    # Model 2: Regression Tree - Sleep Duration
    print("\n" + "-"*80)
    print("MODEL 2: Regression Tree - Sleep Duration (SLD012)")
    print("-"*80)
    
    df_reg = df[feature_cols + ['SLD012']].dropna()
    print(f"Complete cases for regression: {len(df_reg)}")
    
    X_reg = df_reg[feature_cols]
    y_reg = df_reg['SLD012']
    
    X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(
        X_reg, y_reg, test_size=0.3, random_state=42
    )
    
    # Decision Tree Regressor
    dt_regressor = DecisionTreeRegressor(max_depth=5, min_samples_split=50, 
                                        min_samples_leaf=50, random_state=42)
    dt_regressor.fit(X_train_r, y_train_r)
    
    y_pred_train_r = dt_regressor.predict(X_train_r)
    y_pred_test_r = dt_regressor.predict(X_test_r)
    
    train_r2 = r2_score(y_train_r, y_pred_train_r)
    test_r2 = r2_score(y_test_r, y_pred_test_r)
    test_rmse = np.sqrt(mean_squared_error(y_test_r, y_pred_test_r))
    
    print(f"Training R²: {train_r2:.4f}")
    print(f"Test R²: {test_r2:.4f}")
    print(f"Test RMSE: {test_rmse:.4f}")
    
    # Feature importance
    feature_importance_reg = pd.DataFrame({
        'Feature': feature_cols,
        'Importance': dt_regressor.feature_importances_
    }).sort_values('Importance', ascending=False)
    
    print("\nFeature Importance:")
    print(feature_importance_reg)
    
    dt_reg_path = output_path / 'models' / 'decision_tree_regressor_sleep_duration.joblib'
    joblib.dump(dt_regressor, dt_reg_path)

    results['regression'] = {
        'dt_model': dt_regressor,
        'train_r2': train_r2,
        'test_r2': test_r2,
        'test_rmse': test_rmse,
        'feature_importance': feature_importance_reg
    }
    
    # Visualizations
    # Decision Tree Visualization (Classification)
    plt.figure(figsize=(20, 10))
    plot_tree(dt_classifier, feature_names=feature_cols, 
              class_names=['Good Sleep', 'Poor Sleep'], 
              filled=True, rounded=True, fontsize=10)
    plt.title('Decision Tree - Poor Sleep Classification', fontsize=16)
    plt.savefig(f'{output_dir}/figures/decision_tree_classification.png', 
                dpi=300, bbox_inches='tight')
    plt.close()
    
    # Decision Tree Visualization (Regression)
    plt.figure(figsize=(20, 10))
    plot_tree(dt_regressor, feature_names=feature_cols, 
              filled=True, rounded=True, fontsize=10)
    plt.title('Decision Tree - Sleep Duration Regression', fontsize=16)
    plt.savefig(f'{output_dir}/figures/decision_tree_regression.png', 
                dpi=300, bbox_inches='tight')
    plt.close()
    
    # Feature Importance Comparison
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Classification
    feature_importance.plot(x='Feature', y='Importance', kind='barh', 
                           ax=axes[0], color='steelblue')
    axes[0].set_title('Feature Importance - Classification')
    axes[0].set_xlabel('Importance')
    
    # Regression
    feature_importance_reg.plot(x='Feature', y='Importance', kind='barh', 
                               ax=axes[1], color='coral')
    axes[1].set_title('Feature Importance - Regression')
    axes[1].set_xlabel('Importance')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/figures/decision_tree_feature_importance.png', 
                dpi=300, bbox_inches='tight')
    plt.close()
    
    # Confusion Matrix
    cm = confusion_matrix(y_test_c, y_pred_test)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=['Good Sleep', 'Poor Sleep'],
                yticklabels=['Good Sleep', 'Poor Sleep'])
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.title('Confusion Matrix - Poor Sleep Classification')
    plt.savefig(f'{output_dir}/figures/decision_tree_confusion_matrix.png', 
                dpi=300, bbox_inches='tight')
    plt.close()
    
    # Save results
    feature_importance.to_csv(f'{output_dir}/tables/dt_classification_importance.csv', index=False)
    feature_importance_reg.to_csv(f'{output_dir}/tables/dt_regression_importance.csv', index=False)
    
    # Summary table
    summary = pd.DataFrame({
        'Model': ['Classification (Poor Sleep)', 'Regression (Sleep Hours)'],
        'Metric': ['Test Accuracy', 'Test R²'],
        'Value': [test_accuracy, test_r2]
    })
    summary.to_csv(f'{output_dir}/tables/decision_tree_summary.csv', index=False)
    
    return results
