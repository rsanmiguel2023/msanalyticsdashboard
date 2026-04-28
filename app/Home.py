"""Home.py — Landing page for the Microsoft Stock Analytics Dashboard."""
from pathlib import Path
import sys
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "app" / "utils"))
from common import apply_theme, banner, tip_header, load_csv, show_image, FIGURES

st.set_page_config(page_title="MSFT Stock Analytics", page_icon="📈", layout="wide", initial_sidebar_state="expanded")
apply_theme()

st.title("📈 Microsoft Stock Analytics & Predictive Modeling Dashboard")
st.markdown("""
**Project:** Data-Driven Analysis of Microsoft Stock Performance: Exploring Trends and Predictive Indicators  
**Course:** DAMO-611-5 Data Analytics Case Study 3  
**Institution:** University of Niagara Falls Canada

This Streamlit dashboard converts the academic case study into an interactive GitHub portfolio project. It evaluates whether Microsoft historical stock data contains useful patterns for short-term trading decisions through EDA, hypothesis testing, technical indicators, market correlation, and predictive modeling.
""")
st.divider()

banner("Executive Summary — Portfolio Dashboard", "The analysis finds no statistically significant monthly seasonality for MSFT returns, weak evidence that 50/200 moving-average crossovers reliably predict short-term returns, a strong positive relationship between MSFT and QQQ daily returns, and limited next-day directional prediction power from technical indicators. Random Forest and XGBoost perform only slightly above chance, making the project valuable as a disciplined analytics workflow rather than a trading guarantee.")

msft = load_csv("msft_engineered_features.csv", nrows=100000)
rq2 = load_csv("rq2_crossover_results.csv")
rq4 = load_csv("rq4_model_results.csv")

k1,k2,k3,k4 = st.columns(4)
if not msft.empty:
    msft["date"] = pd.to_datetime(msft["date"])
    k1.metric("MSFT Records", f"{len(msft):,}", "Daily observations")
    k2.metric("Date Range", f"{msft['date'].min().year}–{msft['date'].max().year}", "Historical coverage")
else:
    k1.metric("MSFT Records", "N/A")
    k2.metric("Date Range", "N/A")
k3.metric("MA Crossovers", f"{len(rq2):,}" if not rq2.empty else "N/A", "Bullish + bearish signals")
if not rq4.empty:
    best = rq4.loc[rq4["test_roc_auc"].idxmax()]
    k4.metric("Best Test ROC AUC", f"{best['test_roc_auc']:.3f}", best["model"])
else:
    k4.metric("Best Test ROC AUC", "N/A")

st.markdown("---")
left, right = st.columns([1.2, .8])
with left:
    tip_header("Research Questions", "**Research Question Mapping:** The dashboard is organized around the same four analytical questions used in the report, moving from descriptive evidence to predictive modeling.", level=2)
    st.markdown("""
| RQ | Focus | Method | Dashboard Page |
|---|---|---|---|
| **RQ1** | Are there monthly patterns in MSFT returns? | OLS + ANOVA + monthly boxplots | RQ1 Seasonality |
| **RQ2** | Do 50/200 moving-average crossovers lead to meaningful price movement? | Crossover analysis + t-tests + directional modeling | RQ2 MA Crossover |
| **RQ3** | Is MSFT significantly correlated with QQQ? | Pearson correlation + OLS regression | RQ3 MSFT vs QQQ |
| **RQ4** | Can technical indicators predict next-day direction? | Feature engineering + ML classification | RQ4 Modeling |
""")
with right:
    tip_header("Navigation Guide", "**How to use this dashboard:** Start with EDA to understand the raw price behavior, then move through each research question. Each page follows the same format: executive summary, KPI cards, tabs, charts, interpretation, and conclusion.", level=2)
    st.info("Use the left sidebar to open the EDA and RQ pages. Each page includes hover tooltips beside section headers for business and technical interpretation.")

st.markdown("---")
tip_header("Featured Visual", "**Hero Chart:** Long-term MSFT closing price gives the historical context for the full project. It shows the scale of growth, trend shifts, and major volatility periods before modeling.", level=2)
show_image(FIGURES / "eda" / "msft_closing_price.png", "MSFT closing price over time")

st.markdown("---")
tip_header("Repository Structure", "**GitHub Format:** This project follows the same portfolio-ready structure as the capstone repository: source modules, tests, reports, figures, data folders, notebooks, and a Streamlit app.", level=2)
st.code("""msft-stock-analytics-dashboard/
├── app/                 # Streamlit dashboard
├── data/                # raw and processed CSV files
├── figures/             # exported EDA and RQ visuals
├── notebooks/           # original analysis notebooks
├── reports/             # markdown technical documentation
├── src/                 # reusable Python modules
├── tests/               # pytest unit tests
├── README.md
└── requirements.txt""", language="text")
