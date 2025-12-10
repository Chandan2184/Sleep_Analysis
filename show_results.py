"""
Generate a summary of model performance metrics.
"""
import pandas as pd
from pathlib import Path
import sys

# Add src to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / 'src'))

from analysis.regression import perform_regression_analysis
from analysis.decision_trees import perform_decision_tree_analysis

def generate_results_summary():
    """
    Runs the analysis and generates a markdown file with model performance.
    """
    # Load data
    data_path = project_root / 'data' / 'processed' / 'prepared_sleep_analysis_data.csv'
    if not data_path.exists():
        print(f"Error: Data file not found at {data_path}")
        print("Please run 'python run_analysis.py' first to generate the data.")
        return

    df = pd.read_csv(data_path)

    # Run analyses
    regression_results = perform_regression_analysis(df)
    decision_tree_results = perform_decision_tree_analysis(df)

    # Create markdown content
    md_content = "# Model Performance Results\n\n"

    # Regression Models
    md_content += "## Linear Regression Models\n\n"
    md_content += "| Model | R² | MAE | RMSE |\n"
    md_content += "|---|---|---|---|\n"
    for i in range(1, 4):
        model_key = f'model{i}'
        model_name = f"Model {i}"
        r2 = regression_results[model_key]['r2']
        mae = regression_results[model_key]['mae']
        rmse = regression_results[model_key]['rmse']
        md_content += f"| {model_name} | {r2:.4f} | {mae:.4f} | {rmse:.4f} |\n"
    md_content += "\n"

    # Decision Tree Models
    md_content += "## Decision Tree Models\n\n"
    
    # Classification
    class_results = decision_tree_results['classification']
    md_content += "### Classification (Poor Sleep)\n\n"
    md_content += f"- **Test Accuracy:** {class_results['test_accuracy']:.4f}\n"
    md_content += f"- **Random Forest Test Accuracy:** {class_results['rf_accuracy']:.4f}\n\n"

    # Regression
    reg_results = decision_tree_results['regression']
    md_content += "### Regression (Sleep Duration)\n\n"
    md_content += "| Metric | Value |\n"
    md_content += "|---|---|\n"
    md_content += f"| Test R² | {reg_results['test_r2']:.4f} |\n"
    md_content += f"| Test RMSE | {reg_results['test_rmse']:.4f} |\n"
    md_content += "\n"

    # Write to file
    results_path = project_root / 'model_results.md'
    with open(results_path, 'w') as f:
        f.write(md_content)

    print(f"Model performance summary saved to: {results_path}")

if __name__ == '__main__':
    generate_results_summary()