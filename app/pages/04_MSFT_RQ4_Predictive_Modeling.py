"""RQ4 predictive modeling page."""
from pathlib import Path
import sys
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "app" / "utils"))
from common import apply_theme, banner, tip_header, load_csv, show_image, FIGURES

st.set_page_config(page_title="RQ4 — Predictive Modeling", page_icon="🤖", layout="wide")
apply_theme()

st.title("🤖 RQ4: Predicting MSFT Next-Day Price Direction")
st.markdown("""
<p><strong>Research Question:</strong> Can technical indicators predict next-day price direction with greater than 55% accuracy?</p>
<div style="margin-left:1.5rem;"><p><strong>H₀:</strong> Technical indicators do not provide useful predictive power, and model performance is indistinguishable from weak/random prediction.</p><p><strong>H₁:</strong> Technical indicators significantly improve next-day direction prediction performance.</p></div>
<strong>Method:</strong> Feature engineering, correlation filtering, feature importance, 10-fold cross-validation, and model comparison using ROC AUC, accuracy, precision, recall, and F1.
""", unsafe_allow_html=True)
st.divider()

features = load_csv("msft_engineered_features.csv")
results = load_csv("rq4_model_results.csv")
importance = load_csv("rq4_feature_importance.csv")

banner("Executive Summary — RQ4 Result", "The classification models show limited predictive strength. Random Forest has the highest reported ROC AUC at approximately 0.5437 in cross-validation and about 0.535 on the test set, while XGBoost has the strongest F1 among the saved model results. These scores are only slightly better than random guessing, so the project does not support a strong claim that technical indicators can reliably predict MSFT next-day direction.")

if results.empty:
    st.stop()
best_auc = results.loc[results["test_roc_auc"].idxmax()]
best_f1 = results.loc[results["f1"].idxmax()]
selected_features = ["ma_5","std_5","bollinger_width","volatility_regime","volume_change","daily_return","rolling_return_3","momentum_3","momentum_7","rsi_14","rsi_volatility_interaction","price_gap","close_to_ma50","ma_gap_5_20","close_to_range","weekday","month","day","rolling_max_10"]

c1,c2,c3,c4 = st.columns(4)
c1.metric("Best Test ROC AUC", f"{best_auc['test_roc_auc']:.3f}", best_auc["model"])
c2.metric("Best CV ROC AUC", f"{results['cv_roc_auc'].max():.4f}")
c3.metric("Best F1", f"{best_f1['f1']:.3f}", best_f1["model"])
c4.metric("Selected Features", f"{len(selected_features)}")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["🧱 Feature Engineering", "🔥 Correlation", "🏆 Model Results", "⭐ Feature Importance", "🎯 Conclusion"])
with tab1:
    tip_header("Final Modeling Feature Set", "**Feature Set:** Features were engineered to capture trend, volatility, momentum, volume behavior, price gaps, calendar effects, and interactions while avoiding future leakage.", level=3)
    groups = {
        "Trend": ["ma_5","close_to_ma50","ma_gap_5_20"],
        "Volatility": ["std_5","bollinger_width","volatility_regime","rsi_volatility_interaction"],
        "Momentum/Returns": ["daily_return","rolling_return_3","momentum_3","momentum_7","rsi_14"],
        "Volume": ["volume_change"],
        "Price Behavior": ["price_gap","close_to_range","rolling_max_10"],
        "Calendar": ["weekday","month","day"]
    }
    for group, feats in groups.items():
        st.markdown(f"**{group}:** " + ", ".join(f"`{f}`" for f in feats))
    if not features.empty:
        cols = ["date"] + [f for f in selected_features if f in features.columns] + ["target"]
        st.dataframe(features[cols].tail(10), use_container_width=True)
with tab2:
    tip_header("Correlation Matrix of Engineered Features", "**Correlation Filtering:** Highly correlated features can create redundancy and overfitting. The project used correlation analysis to reduce multicollinearity before model comparison.", level=3)
    show_image(FIGURES / "rq4" / "feature_correlation_heatmap.png")
    st.markdown("**Interpretation:** Several moving-average and volatility variables are highly related, so the reduced modeling set keeps representative variables instead of many duplicates.")
with tab3:
    tip_header("Model Performance Comparison", "**ROC AUC:** ROC AUC measures whether the model ranks upward days above downward days. A value near 0.50 is close to random guessing.", level=3)
    show_image(FIGURES / "rq4" / "model_roc_auc_comparison.png")
    fig = px.bar(results, x="model", y="test_roc_auc", title="Test ROC AUC by Model", text="test_roc_auc")
    fig.add_hline(y=0.50, line_dash="dash", annotation_text="Random baseline")
    fig.add_hline(y=0.55, line_dash="dot", annotation_text="Project target")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(results, use_container_width=True)
with tab4:
    tip_header("Feature Importance", "**Feature Importance:** Tree-based models can estimate which variables contribute more to prediction decisions, but importance does not prove causation.", level=3)
    show_image(FIGURES / "rq4" / "random_forest_feature_importance.png")
    if not importance.empty:
        fig = px.bar(importance.sort_values("importance", ascending=True), x="importance", y="feature", orientation="h", title="Saved Feature Importance Values")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(importance, use_container_width=True)
with tab5:
    tip_header("RQ4 Final Conclusion", "**Conclusion:** The model pipeline is valid as a portfolio analytics workflow, but the actual predictive strength is weak. This is common in short-term stock direction prediction.", level=3)
    st.warning("RQ4 Conclusion: Technical indicators provide only limited predictive power for MSFT next-day direction in this project. Random Forest and XGBoost are slightly better than random, but not strong enough to support reliable trading decisions.")
    st.markdown("**Portfolio framing:** This is still a strong project because it demonstrates a complete machine learning workflow: feature engineering, leakage-aware target creation, correlation filtering, cross-validation, model comparison, feature importance, and honest interpretation of weak market predictability.")
