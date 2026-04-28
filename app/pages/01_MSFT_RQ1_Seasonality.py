"""RQ1 Seasonality page."""
from pathlib import Path
import sys
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "app" / "utils"))
from common import apply_theme, banner, tip_header, load_csv, show_image, FIGURES

st.set_page_config(page_title="RQ1 — Seasonality", page_icon="📅", layout="wide")
apply_theme()

st.title("📅 RQ1: Monthly Return Seasonality")
st.markdown("""
<p><strong>Research Question:</strong> Are there seasonal or monthly patterns in Microsoft’s stock returns from 2014 to 2024?</p>
<div style="margin-left:1.5rem;"><p><strong>H₀:</strong> The average returns across all twelve calendar months are equal.</p><p><strong>H₁:</strong> At least one month has a significantly different average return.</p></div>
<strong>Method:</strong> Monthly return visualization + OLS regression + ANOVA test.
""", unsafe_allow_html=True)
st.divider()

rq1 = load_csv("rq1_monthly_returns.csv")
banner("Executive Summary — RQ1 Result", "The ANOVA result does not support a statistically significant monthly effect in MSFT daily returns for 2014–2024. The reported p-value is above 0.05, so the null hypothesis is not rejected. Some months show wider spread and outliers, but these visual differences are not strong enough to confirm seasonality.")
if rq1.empty:
    st.stop()
rq1["date"] = pd.to_datetime(rq1["date"])

f_stat, p_val, r_squared = 0.9391, 0.5012, 0.004
c1,c2,c3,c4 = st.columns(4)
c1.metric("F-Statistic", f"{f_stat:.4f}")
c2.metric("p-value", f"{p_val:.4f}", "p > 0.05")
c3.metric("R²", f"{r_squared:.3f}", "< 1% explained")
c4.metric("Decision", "Fail to Reject H₀", "No significant seasonality")

tab1, tab2, tab3, tab4 = st.tabs(["📊 Monthly Boxplot", "📈 Monthly Summary", "🧪 ANOVA Interpretation", "🎯 Conclusion"])
with tab1:
    tip_header("Monthly Return Boxplot", "**Monthly Boxplot:** This chart compares the distribution of daily returns across all calendar months. It helps reveal median differences, spread, and outliers before statistical testing.", level=3)
    show_image(FIGURES / "rq1" / "monthly_return_boxplot.png")
    st.markdown("**Interpretation:** Median returns appear close across months, while March and October show more variability. The formal test is still required because visual differences alone are not proof of seasonality.")
with tab2:
    tip_header("Average Return by Month", "**Monthly Summary:** Aggregating daily returns by month gives a simpler view of monthly tendencies, but it should not replace the full distribution and hypothesis test.", level=3)
    summary = rq1.groupby("month").agg(avg_daily_return=("daily_return","mean"), std_daily_return=("daily_return","std"), observations=("daily_return","count")).reset_index()
    fig = px.bar(summary, x="month", y="avg_daily_return", title="Average Daily Return by Month, 2014–2024")
    fig.update_layout(yaxis_tickformat=".2%")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(summary, use_container_width=True)
with tab3:
    tip_header("ANOVA Test Decision", "**ANOVA:** The test asks whether at least one month has a statistically different average daily return. A p-value above 0.05 means the evidence is not strong enough to reject equal monthly means.", level=3)
    st.markdown(f"""| Test Output | Value | Interpretation |
|---|---:|---|
| F-statistic | {f_stat:.4f} | Between-month variation is small relative to within-month noise |
| p-value | {p_val:.4f} | Not statistically significant at α = 0.05 |
| R² | {r_squared:.3f} | Month explains less than 1% of return variation |
| Decision | Fail to reject H₀ | No reliable monthly seasonality detected |""")
    st.info("Business meaning: monthly timing alone is not strong enough to guide MSFT short-term trading decisions in this dataset.")
with tab4:
    tip_header("RQ1 Final Conclusion", "**Conclusion:** The correct portfolio interpretation is disciplined and conservative: visual volatility differences exist, but statistical evidence does not confirm a meaningful monthly return pattern.", level=3)
    st.success("RQ1 Conclusion: There is no statistically significant evidence that MSFT daily returns differ by calendar month from 2014–2024.")
