"""RQ3 MSFT vs QQQ correlation page."""
from pathlib import Path
import sys
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "app" / "utils"))
from common import apply_theme, banner, tip_header, load_csv, show_image, FIGURES

st.set_page_config(page_title="RQ3 — MSFT vs QQQ", page_icon="🔗", layout="wide")
apply_theme()

st.title("🔗 RQ3: MSFT Return Relationship with QQQ")
st.markdown("""
<p><strong>Research Question:</strong> Is there a statistically significant correlation between Microsoft’s daily returns and those of the Nasdaq-100 ETF (QQQ)?</p>
<div style="margin-left:1.5rem;"><p><strong>H₀:</strong> There is no correlation between Microsoft’s and QQQ’s daily returns.</p><p><strong>H₁:</strong> There is a significant positive correlation between Microsoft’s and QQQ’s daily returns.</p></div>
<strong>Method:</strong> Pearson correlation, scatter plot, and OLS regression.
""", unsafe_allow_html=True)
st.divider()

rq3 = load_csv("rq3_msft_qqq_returns.csv")
banner("Executive Summary — RQ3 Result", "MSFT daily returns have a strong, statistically significant positive relationship with QQQ returns. The project report shows a regression coefficient of approximately 1.0764 and R² of 0.732, meaning QQQ returns explain about 73.2% of variation in MSFT daily returns over the tested period.")
if rq3.empty:
    st.stop()
rq3["date"] = pd.to_datetime(rq3["date"])
correlation = rq3["msft_return"].corr(rq3["qqq_return"])
reported_beta, reported_r2, reported_n, reported_f = 1.0764, 0.732, 2515, 6855.569

c1,c2,c3,c4 = st.columns(4)
c1.metric("Pearson r", f"{correlation:.3f}")
c2.metric("OLS β(QQQ)", f"{reported_beta:.4f}")
c3.metric("R²", f"{reported_r2:.3f}")
c4.metric("Observations", f"{reported_n:,}")

tab1, tab2, tab3, tab4 = st.tabs(["📉 Scatter Plot", "📈 Time Pattern", "🧪 Regression Result", "🎯 Conclusion"])
with tab1:
    tip_header("MSFT vs QQQ Daily Returns", "**Scatter Plot:** Each dot is one trading day. A strong upward pattern means MSFT and QQQ tend to move in the same direction.", level=3)
    show_image(FIGURES / "rq3" / "msft_vs_qqq_scatter.png")
    st.markdown("**Interpretation:** The relationship is strong and positive, which is expected because MSFT is a major technology stock and QQQ tracks the Nasdaq-100 ETF.")
with tab2:
    tip_header("Return Time Series", "**Time Series View:** This view shows whether MSFT and QQQ return movements line up over time, especially during high-volatility periods.", level=3)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=rq3["date"], y=rq3["msft_return"], mode="lines", name="MSFT return"))
    fig.add_trace(go.Scatter(x=rq3["date"], y=rq3["qqq_return"], mode="lines", name="QQQ return"))
    fig.update_layout(title="MSFT and QQQ Daily Returns Over Time", yaxis_tickformat=".2%")
    st.plotly_chart(fig, use_container_width=True)
with tab3:
    tip_header("OLS Regression Summary", "**OLS Regression:** This estimates how much MSFT daily return changes, on average, for a 1 percentage point change in QQQ daily return.", level=3)
    st.markdown(f"""| Regression Metric | Value | Interpretation |
|---|---:|---|
| Coefficient for QQQ | {reported_beta:.4f} | A 1% QQQ move is associated with about a 1.08% MSFT move |
| R² | {reported_r2:.3f} | QQQ explains 73.2% of MSFT return variation |
| F-statistic | {reported_f:,.3f} | Overall model is strongly significant |
| p-value | < 0.001 | Reject H₀ |""")
    st.info("Business meaning: MSFT movement is strongly tied to the broader technology-heavy market, so market context should be considered in any trading model.")
with tab4:
    tip_header("RQ3 Final Conclusion", "**Conclusion:** The relationship is statistically and practically strong. This supports using broader market context when interpreting MSFT behavior.", level=3)
    st.success("RQ3 Conclusion: MSFT and QQQ daily returns have a strong, statistically significant positive relationship.")
