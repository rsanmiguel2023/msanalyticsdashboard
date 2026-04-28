"""EDA page for MSFT stock project."""
from pathlib import Path
import sys
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "app" / "utils"))
from common import apply_theme, banner, tip_header, load_csv, show_image, FIGURES

st.set_page_config(page_title="EDA — MSFT", page_icon="🔍", layout="wide")
apply_theme()

st.title("🔍 Exploratory Data Analysis — MSFT Stock")
st.markdown("This page explores the structure, trend, return distribution, volume behavior, volatility, and calendar patterns of Microsoft historical stock data before hypothesis testing and model building.")
st.divider()

msft = load_csv("msft_engineered_features.csv")
banner("Executive Summary — EDA Findings", "MSFT shows strong long-term price appreciation, especially after 2010, while daily returns remain centered near zero with fat tails typical of financial time series. Trading volume spikes during major market events, and rolling volatility rises sharply during stress periods such as the COVID-19 market shock. Calendar patterns are visually weak and require formal testing in RQ1.")

if msft.empty:
    st.stop()
msft["date"] = pd.to_datetime(msft["date"])

c1,c2,c3,c4 = st.columns(4)
c1.metric("Rows", f"{len(msft):,}")
c2.metric("Start Date", msft["date"].min().strftime("%Y-%m-%d"))
c3.metric("End Date", msft["date"].max().strftime("%Y-%m-%d"))
c4.metric("Latest Close", f"${msft['close'].dropna().iloc[-1]:,.2f}")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Price Trend", "📊 Returns", "📦 Volume", "🌪️ Volatility", "🗓️ Calendar"])

with tab1:
    tip_header("MSFT Closing Price Over Time", "**Price Trend:** This chart provides the long-term context for the project. Large upward movement after 2010 makes raw price features highly trended, so modeling relies on returns, ratios, volatility, and momentum features instead of only close price.", level=3)
    show_image(FIGURES / "eda" / "msft_closing_price.png")
    st.markdown("**Interpretation:** The chart supports using technical indicators because MSFT has experienced major trend regimes over the full historical period.")

with tab2:
    tip_header("Distribution of Daily Returns", "**Daily Returns:** Returns are more appropriate than raw prices for statistical testing because they measure percentage movement from one trading day to the next.", level=3)
    show_image(FIGURES / "eda" / "daily_return_distribution.png")
    ret = msft["daily_return"].dropna()
    r1,r2,r3,r4 = st.columns(4)
    r1.metric("Mean Daily Return", f"{ret.mean()*100:.4f}%")
    r2.metric("Std Dev", f"{ret.std()*100:.2f}%")
    r3.metric("Min", f"{ret.min()*100:.2f}%")
    r4.metric("Max", f"{ret.max()*100:.2f}%")

with tab3:
    tip_header("Trading Volume Over Time", "**Volume Behavior:** Volume can reflect market participation, news reactions, earnings activity, and market stress. Volume change is later used as a predictive feature in RQ4.", level=3)
    show_image(FIGURES / "eda" / "trading_volume.png")
    st.markdown("**Interpretation:** Large spikes suggest periods where investor activity changed sharply, which may influence short-term price behavior.")

with tab4:
    tip_header("Rolling Volatility", "**Rolling Volatility:** 5-day and 20-day rolling standard deviations capture short-term and medium-term risk. These features help identify calm vs turbulent regimes.", level=3)
    show_image(FIGURES / "eda" / "rolling_volatility.png")
    v1,v2,v3 = st.columns(3)
    v1.metric("Avg 5-Day Std", f"{msft['std_5'].dropna().mean():.4f}")
    v2.metric("Avg 20-Day Std", f"{msft['std_20'].dropna().mean():.4f}")
    v3.metric("High Volatility Days", f"{int(msft['volatility_regime'].sum()):,}")

with tab5:
    tip_header("Calendar Return Patterns", "**Calendar Patterns:** Weekday and month features test whether returns behave differently depending on the trading calendar. Formal monthly testing is handled in RQ1.", level=3)
    monthly = msft.dropna(subset=["daily_return"]).groupby("month", as_index=False)["daily_return"].mean()
    fig = px.bar(monthly, x="month", y="daily_return", title="Average Daily Return by Month")
    fig.update_layout(yaxis_tickformat=".2%")
    st.plotly_chart(fig, use_container_width=True)
    weekday = msft.dropna(subset=["daily_return"]).groupby("weekday", as_index=False)["daily_return"].mean()
    fig2 = px.bar(weekday, x="weekday", y="daily_return", title="Average Daily Return by Weekday (0=Monday)")
    fig2.update_layout(yaxis_tickformat=".2%")
    st.plotly_chart(fig2, use_container_width=True)
