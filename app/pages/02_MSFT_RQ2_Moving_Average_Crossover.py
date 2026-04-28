"""RQ2 Moving average crossover page."""
from pathlib import Path
import sys
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "app" / "utils"))
from common import apply_theme, banner, tip_header, load_csv, show_image, FIGURES

st.set_page_config(page_title="RQ2 — MA Crossover", page_icon="🔀", layout="wide")
apply_theme()

st.title("🔀 RQ2: 50-Day / 200-Day Moving Average Crossovers")
st.markdown("""
<p><strong>Research Question:</strong> Do 50-day and 200-day moving average crossovers lead to statistically significant stock price movement from 2014 to 2024?</p>
<div style="margin-left:1.5rem;"><p><strong>H₀:</strong> There is no significant change in stock price following a moving average crossover.</p><p><strong>H₁:</strong> Stock prices change significantly following a moving average crossover.</p></div>
<strong>Method:</strong> Technical indicator crossover detection, bullish/bearish return comparison, Welch’s t-tests, and exploratory directional modeling.
""", unsafe_allow_html=True)
st.divider()

rq2 = load_csv("rq2_crossover_results.csv")
banner("Executive Summary — RQ2 Result", "Bullish crossovers visually show higher median returns than bearish crossovers across 3-day, 5-day, and 10-day horizons, but the reported tests do not reach conventional statistical significance. Therefore, moving-average crossovers may be useful for visual trend context but are not confirmed as reliable standalone short-term trading signals in this project.")
if rq2.empty:
    st.stop()
rq2["date"] = pd.to_datetime(rq2["date"])

bullish = (rq2["crossover_type"].str.lower() == "bullish").sum()
bearish = (rq2["crossover_type"].str.lower() == "bearish").sum()
mean5_bull = rq2.loc[rq2["crossover_type"].str.lower() == "bullish", "return_5d"].mean()
mean5_bear = rq2.loc[rq2["crossover_type"].str.lower() == "bearish", "return_5d"].mean()

c1,c2,c3,c4 = st.columns(4)
c1.metric("Total Crossovers", f"{len(rq2):,}")
c2.metric("Bullish", f"{bullish:,}")
c3.metric("Bearish", f"{bearish:,}")
c4.metric("5-Day Spread", f"{(mean5_bull-mean5_bear)*100:.2f}%")

tab1, tab2, tab3, tab4 = st.tabs(["📈 Crossover Chart", "📊 Return Horizons", "🧪 Model Result", "🎯 Conclusion"])
with tab1:
    tip_header("Moving Average Crossover Chart", "**MA Crossover:** A bullish signal occurs when the 50-day moving average crosses above the 200-day moving average. A bearish signal occurs when it crosses below. This is a common technical-analysis indicator.", level=3)
    show_image(FIGURES / "rq2" / "moving_average_crossover.png")
    st.markdown("**Interpretation:** Crossovers mark possible trend shifts, but the project tests whether those signals are statistically useful after the event.")
with tab2:
    tip_header("Multi-Day Returns After Crossovers", "**Return Horizons:** Comparing 3-day, 5-day, and 10-day post-crossover returns shows whether the signal has short-term follow-through.", level=3)
    long = rq2.melt(id_vars=["date","crossover_type"], value_vars=["return_3d","return_5d","return_10d"], var_name="horizon", value_name="return")
    fig = px.box(long, x="horizon", y="return", color="crossover_type", title="Post-Crossover Return Distribution")
    fig.update_layout(yaxis_tickformat=".2%")
    st.plotly_chart(fig, use_container_width=True)
    summary = long.groupby(["crossover_type","horizon"]).agg(mean_return=("return","mean"), median_return=("return","median"), n=("return","count")).reset_index()
    st.dataframe(summary, use_container_width=True)
with tab3:
    tip_header("Directional Modeling After Crossovers", "**Model Result:** The project tested whether engineered indicators after crossover events could predict 5-day direction. The logistic model performed weakly, indicating limited practical predictive reliability.", level=3)
    st.markdown("""| Model Output | Reported Result | Meaning |
|---|---:|---|
| Logistic Regression Accuracy | 42.9% | Below the practical target |
| ROC-AUC | 0.1667 | Very weak discrimination |
| Positive-Class Recall | 75% | Captures some bullish cases but misses bearish classification |
| Final Interpretation | Limited reliability | Crossovers alone are not enough |""")
    st.warning("Portfolio wording: this is a valuable negative finding. It shows that the project tested a popular market belief instead of assuming it works.")
with tab4:
    tip_header("RQ2 Final Conclusion", "**Conclusion:** The visual pattern is directionally interesting but statistically weak. A good portfolio project should report this honestly because it demonstrates analytical maturity.", level=3)
    st.success("RQ2 Conclusion: Moving-average crossovers show mild visual directional bias, but the evidence is not strong enough to validate them as reliable short-term predictive signals for MSFT.")
