#!/bin/bash
# Analysis Execution Script
# Run this script to execute the complete analysis pipeline

cd "$(dirname "$0")"
echo "=========================================="
echo "Sleep Quality Analysis Pipeline"
echo "=========================================="
echo ""

# Step 1: Data Preparation
echo "Step 1: Preparing data..."
python3 scripts/01_prepare_data.py
if [ $? -ne 0 ]; then
    echo "ERROR: Data preparation failed"
    exit 1
fi
echo ""

# Step 2: Clustering
echo "Step 2: Running K-means clustering..."
python3 scripts/02_clustering.py
echo ""

# Step 3: Regression
echo "Step 3: Running linear regression..."
python3 scripts/03_regression.py
echo ""

# Step 4: Decision Trees
echo "Step 4: Running decision tree analysis..."
python3 scripts/04_decision_trees.py
echo ""

echo "=========================================="
echo "Analysis Complete!"
echo "=========================================="
echo "Results saved in:"
echo "  - results/figures/  (visualizations)"
echo "  - results/tables/   (summary tables)"
echo "  - data/processed/   (prepared dataset)"

