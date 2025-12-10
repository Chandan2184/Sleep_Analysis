#!/usr/bin/env python3
"""
Streamlit UI to explore saved model artifacts.
Launch with: streamlit run scripts/model_viewer.py
"""

import joblib
import streamlit as st
from pathlib import Path
import pandas as pd
import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODELS_DIR = PROJECT_ROOT / "results" / "models"
TABLES_DIR = PROJECT_ROOT / "results" / "tables"


def safe_load(path: Path):
    if not path.exists():
        st.warning(f"Missing: {path.name}")
        return None
    try:
        return joblib.load(path)
    except Exception as exc:  # pragma: no cover - UI helper
        st.error(f"Failed to load {path.name}: {exc}")
        return None


st.set_page_config(page_title="Sleep Analysis Models", layout="wide")
st.title("Sleep Quality Analysis – Model Viewer")
st.caption("Browse saved joblib models and key artifacts.")

st.sidebar.header("Artifacts")
st.sidebar.write(f"Models dir: `{MODELS_DIR}`")
st.sidebar.write(f"Tables dir: `{TABLES_DIR}`")

# ---- Clustering ----
st.header("K-Means Clustering")
kmeans = safe_load(MODELS_DIR / "kmeans_clustering.joblib")
scaler = safe_load(MODELS_DIR / "kmeans_scaler.joblib")
cluster_features = [
    "SMOKING_STATUS",
    "ALCOHOL_STATUS",
    "RIDAGEYR",
    "RIAGENDR",
    "INDFMPIR",
    "CIGARETTES_PER_DAY",
    "AVG_DRINKS_DAY",
]

if kmeans is not None:
    st.subheader("Model Info")
    st.write({"n_clusters": kmeans.n_clusters, "inertia": getattr(kmeans, "inertia_", None)})

    centers = pd.DataFrame(kmeans.cluster_centers_, columns=cluster_features)
    st.subheader("Cluster Centers (scaled)")
    st.dataframe(centers, use_container_width=True)

    if scaler is not None and hasattr(scaler, "inverse_transform"):
        try:
            centers_unscaled = pd.DataFrame(
                scaler.inverse_transform(kmeans.cluster_centers_),
                columns=cluster_features,
            )
            st.subheader("Cluster Centers (original scale)")
            st.dataframe(centers_unscaled, use_container_width=True)
        except Exception:
            st.info("Could not inverse-transform cluster centers; showing scaled values only.")

    cluster_table = TABLES_DIR / "cluster_characteristics.csv"
    if cluster_table.exists():
        st.subheader("Cluster Characteristics")
        st.dataframe(pd.read_csv(cluster_table), use_container_width=True)

# ---- Regression (Statsmodels OLS) ----
st.header("Linear Regression (OLS)")
reg_files = {
    "Sleep Duration (Model 1)": "regression_model1_sleep_duration.joblib",
    "Sleep Quality (Model 2)": "regression_model2_sleep_quality.joblib",
    "Daytime Sleepiness (Model 3)": "regression_model3_daytime_sleepiness.joblib",
}

for label, fname in reg_files.items():
    model = safe_load(MODELS_DIR / fname)
    if model is None:
        continue
    with st.expander(label, expanded=False):
        st.write("Coefficients")
        st.dataframe(model.params.to_frame("coef"), use_container_width=True)
        st.markdown(f"**R²:** {getattr(model, 'rsquared', 'n/a'):.4f}")
        st.markdown(f"**Adj. R²:** {getattr(model, 'rsquared_adj', 'n/a'):.4f}")
        st.text(model.summary())

# ---- Decision Trees / Random Forest ----
st.header("Decision Trees and Random Forest")
dt_clf = safe_load(MODELS_DIR / "decision_tree_classifier_poor_sleep.joblib")
rf_clf = safe_load(MODELS_DIR / "random_forest_classifier_poor_sleep.joblib")
dt_reg = safe_load(MODELS_DIR / "decision_tree_regressor_sleep_duration.joblib")

dt_features = [
    "SMOKING_STATUS",
    "ALCOHOL_STATUS",
    "CIGARETTES_PER_DAY",
    "AVG_DRINKS_DAY",
    "RIDAGEYR",
    "RIAGENDR",
    "INDFMPIR",
]

if dt_clf is not None:
    st.subheader("Decision Tree – Poor Sleep (Classifier)")
    st.write({"depth": dt_clf.get_depth(), "leaves": dt_clf.get_n_leaves()})
    st.bar_chart(pd.Series(dt_clf.feature_importances_, index=dt_features))

if rf_clf is not None:
    st.subheader("Random Forest – Poor Sleep (Classifier)")
    st.write({"n_estimators": len(rf_clf.estimators_), "depth": rf_clf.max_depth})
    st.bar_chart(pd.Series(rf_clf.feature_importances_, index=dt_features))

if dt_reg is not None:
    st.subheader("Decision Tree – Sleep Duration (Regressor)")
    st.write({"depth": dt_reg.get_depth(), "leaves": dt_reg.get_n_leaves()})
    st.bar_chart(pd.Series(dt_reg.feature_importances_, index=dt_features))

st.info("To launch: `streamlit run scripts/model_viewer.py` (activate the venv first).")
