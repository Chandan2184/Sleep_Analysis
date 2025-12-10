"""
K-Means Clustering Analysis
Identify lifestyle clusters based on smoking, alcohol, and demographics
"""

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import joblib


def prepare_clustering_data(df):
    """
    Prepare data for clustering analysis
    
    Parameters:
    -----------
    df : DataFrame
        Input dataframe
    
    Returns:
    --------
    tuple : (X_scaled, feature_names, df_complete)
        Scaled features, feature names, and complete cases dataframe
    """
    # Select features for clustering
    features = [
        'SMOKING_STATUS', 'ALCOHOL_STATUS', 'RIDAGEYR', 
        'RIAGENDR', 'INDFMPIR', 'CIGARETTES_PER_DAY', 'AVG_DRINKS_DAY'
    ]
    
    # Get complete cases
    df_complete = df[features + ['SEQN']].dropna()
    
    # Separate features
    X = df_complete[features].copy()
    
    # Encode categorical variables
    if 'SMOKING_STATUS' in X.columns:
        X['SMOKING_STATUS'] = X['SMOKING_STATUS'].astype(float)
    if 'ALCOHOL_STATUS' in X.columns:
        X['ALCOHOL_STATUS'] = X['ALCOHOL_STATUS'].astype(float)
    if 'RIAGENDR' in X.columns:
        X['RIAGENDR'] = X['RIAGENDR'].astype(float)
    
    # Standardize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    return X_scaled, features, df_complete, scaler


def find_optimal_clusters(X_scaled, max_k=8):
    """
    Find optimal number of clusters using elbow method and silhouette score
    
    Parameters:
    -----------
    X_scaled : array
        Scaled feature matrix
    max_k : int
        Maximum number of clusters to test
    
    Returns:
    --------
    dict
        Results with optimal k and metrics
    """
    from sklearn.metrics import silhouette_score
    
    inertias = []
    silhouette_scores = []
    k_range = range(2, max_k + 1)
    
    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(X_scaled)
        inertias.append(kmeans.inertia_)
        silhouette_scores.append(silhouette_score(X_scaled, kmeans.labels_))
    
    # Find optimal k (elbow + highest silhouette)
    optimal_k = k_range[np.argmax(silhouette_scores)]
    
    return {
        'k_range': list(k_range),
        'inertias': inertias,
        'silhouette_scores': silhouette_scores,
        'optimal_k': optimal_k
    }


def perform_kmeans_clustering(df, n_clusters=4, output_dir='results'):
    """
    Perform K-means clustering analysis
    
    Parameters:
    -----------
    df : DataFrame
        Input dataframe
    n_clusters : int
        Number of clusters (None to auto-select)
    output_dir : str
        Directory to save results
    
    Returns:
    --------
    dict
        Clustering results
    """
    print("\n" + "="*80)
    print("K-MEANS CLUSTERING ANALYSIS")
    print("="*80)
    
    # Prepare data
    X_scaled, feature_names, df_complete, scaler = prepare_clustering_data(df)
    print(f"\nComplete cases for clustering: {len(df_complete)}")
    
    # Find optimal clusters if not specified
    if n_clusters is None:
        print("\nFinding optimal number of clusters...")
        optimal_results = find_optimal_clusters(X_scaled)
        n_clusters = optimal_results['optimal_k']
        print(f"Optimal number of clusters: {n_clusters}")
        
        # Plot elbow and silhouette
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        ax1.plot(optimal_results['k_range'], optimal_results['inertias'], 'bo-')
        ax1.set_xlabel('Number of Clusters (k)')
        ax1.set_ylabel('Inertia')
        ax1.set_title('Elbow Method')
        ax1.grid(True)
        
        ax2.plot(optimal_results['k_range'], optimal_results['silhouette_scores'], 'ro-')
        ax2.set_xlabel('Number of Clusters (k)')
        ax2.set_ylabel('Silhouette Score')
        ax2.set_title('Silhouette Score')
        ax2.grid(True)
        
        plt.tight_layout()
        plt.savefig(f'{output_dir}/figures/clustering_optimal_k.png', dpi=300)
        plt.close()
    
    # Perform clustering
    print(f"\nPerforming K-means clustering with k={n_clusters}...")
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(X_scaled)
    
    # Add cluster labels to dataframe
    df_complete['CLUSTER'] = cluster_labels
    
    # Analyze cluster characteristics
    print("\nCluster Characteristics:")
    print("-" * 80)
    
    cluster_summary = df_complete.groupby('CLUSTER').agg({
        'SMOKING_STATUS': 'mean',
        'ALCOHOL_STATUS': 'mean',
        'RIDAGEYR': 'mean',
        'INDFMPIR': 'mean',
        'CIGARETTES_PER_DAY': 'mean',
        'AVG_DRINKS_DAY': 'mean',
        'SEQN': 'count'
    }).round(2)

    # Gender is coded 1=Male, 2=Female. Show mode and % male instead of a mean.
    gender_mode = df_complete.groupby('CLUSTER')['RIAGENDR'].agg(
        lambda s: s.mode().iloc[0] if not s.mode().empty else np.nan
    )
    gender_pct_male = df_complete.groupby('CLUSTER')['RIAGENDR'].apply(
        lambda s: (s == 1).mean()
    ).round(2)

    cluster_summary['Gender_Mode'] = gender_mode
    cluster_summary['Male_Pct'] = gender_pct_male
    
    cluster_summary = cluster_summary[['SMOKING_STATUS', 'ALCOHOL_STATUS', 'RIDAGEYR',
                                       'Gender_Mode', 'Male_Pct', 'INDFMPIR',
                                       'CIGARETTES_PER_DAY', 'AVG_DRINKS_DAY', 'SEQN']]
    
    cluster_summary.columns = ['Smoking_Status', 'Alcohol_Status', 'Age',
                              'Gender_Mode', 'Male_Pct', 'Income_Ratio',
                              'Cigarettes/Day', 'Drinks/Day', 'N']
    # Show all columns so categorical summaries are visible
    print(cluster_summary.to_string())
    
    # Compare sleep outcomes by cluster
    df_with_clusters = df.merge(df_complete[['SEQN', 'CLUSTER']], on='SEQN', how='left')
    
    sleep_by_cluster = df_with_clusters.groupby('CLUSTER').agg({
        'SLD012': 'mean',
        'SLQ030': 'mean',
        'SLQ120': 'mean',
        'POOR_SLEEP': 'mean',
        'SEQN': 'count'
    }).round(2)
    
    print("\nSleep Outcomes by Cluster:")
    print("-" * 80)
    print(sleep_by_cluster)
    
    # Visualizations
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    (output_path / 'figures').mkdir(exist_ok=True)
    (output_path / 'models').mkdir(exist_ok=True)
    
    # PCA for 2D visualization
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)
    
    plt.figure(figsize=(12, 8))
    scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1], c=cluster_labels, 
                         cmap='viridis', alpha=0.6, s=50)
    plt.colorbar(scatter, label='Cluster')
    plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.2%} variance)')
    plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.2%} variance)')
    plt.title('K-Means Clustering Results (PCA Projection)')
    plt.grid(True, alpha=0.3)
    plt.savefig(f'{output_dir}/figures/clustering_pca.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Cluster characteristics plot
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Sleep outcomes by cluster
    sleep_cols = ['SLD012', 'SLQ030', 'SLQ120', 'POOR_SLEEP']
    for idx, col in enumerate(sleep_cols):
        ax = axes[idx // 2, idx % 2]
        cluster_means = df_with_clusters.groupby('CLUSTER')[col].mean()
        cluster_means.plot(kind='bar', ax=ax, color='steelblue')
        ax.set_title(f'{col} by Cluster')
        ax.set_xlabel('Cluster')
        ax.set_ylabel(col)
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/figures/clustering_sleep_outcomes.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Save results
    cluster_summary.to_csv(f'{output_dir}/tables/cluster_characteristics.csv')
    sleep_by_cluster.to_csv(f'{output_dir}/tables/sleep_by_cluster.csv')
    
    model_path = output_path / 'models' / 'kmeans_clustering.joblib'
    scaler_path = output_path / 'models' / 'kmeans_scaler.joblib'
    joblib.dump(kmeans, model_path)
    joblib.dump(scaler, scaler_path)

    return {
        'model': kmeans,
        'labels': cluster_labels,
        'scaler': scaler,
        'df_with_clusters': df_with_clusters,
        'n_clusters': n_clusters,
        'cluster_summary': cluster_summary,
        'sleep_by_cluster': sleep_by_cluster
    }
