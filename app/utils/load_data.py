from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]

@st.cache_data
def load_msft_engineered():
    return pd.read_csv(ROOT / 'data' / 'processed' / 'msft_engineered_features.csv', parse_dates=['date'])

@st.cache_data
def load_rq3():
    return pd.read_csv(ROOT / 'data' / 'processed' / 'rq3_msft_qqq_returns.csv', parse_dates=['date'])

@st.cache_data
def load_model_results():
    return pd.read_csv(ROOT / 'data' / 'processed' / 'rq4_model_results.csv')

@st.cache_data
def load_feature_importance():
    return pd.read_csv(ROOT / 'data' / 'processed' / 'rq4_feature_importance.csv')
