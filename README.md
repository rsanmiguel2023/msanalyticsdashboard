Here’s your **clean, copy-paste README (no icons, includes your Streamlit link):**

---

# Microsoft Stock Analytics & Predictive Modeling Dashboard

End-to-end data analytics project analyzing Microsoft (MSFT) stock performance using statistical analysis, machine learning, and an interactive Streamlit dashboard.

---

## Live Dashboard

[https://msanalyticsdashboard.streamlit.app/](https://msanalyticsdashboard.streamlit.app/)

---

## Project Overview

This project analyzes Microsoft stock (2014–2024) using a structured analytics framework that combines:

* Exploratory Data Analysis (EDA)
* Statistical hypothesis testing
* Machine learning modeling
* Trading strategy evaluation
* Interactive dashboard (Streamlit)

The goal is to evaluate whether technical indicators and historical patterns provide meaningful insights or predictive power for stock price movements.

---

## Business Problem

Financial markets are highly dynamic and difficult to predict. This project addresses:

* Can we identify consistent return patterns?
* Do technical trading strategies provide value?
* How strongly is MSFT tied to the broader market (QQQ)?
* Can we predict next-day stock direction?

---

## Research Questions

| RQ  | Question                                     | Method                     |
| --- | -------------------------------------------- | -------------------------- |
| RQ1 | Does MSFT exhibit monthly seasonality?       | ANOVA                      |
| RQ2 | Do moving average crossovers signal returns? | Strategy analysis          |
| RQ3 | How correlated is MSFT with QQQ?             | Correlation and regression |
| RQ4 | Can ML predict next-day direction?           | Classification models      |

---

## Key Insights

* No strong monthly seasonality detected
* Moving average signals show weak statistical support
* Strong correlation with QQQ (market-driven behavior)
* Machine learning models perform near random (~50% accuracy)

Conclusion:
MSFT price movement is largely market-driven and difficult to predict using technical indicators alone.

---

## Tech Stack

* Python (Pandas, NumPy, Scikit-learn, XGBoost)
* Matplotlib, Seaborn, Plotly
* Streamlit
* Yahoo Finance data

---

## Feature Engineering

* Moving averages (50-day, 200-day)
* Volatility (rolling standard deviation)
* Momentum (3-day, 7-day)
* RSI (Relative Strength Index)
* Price gap features
* Calendar features (weekday, month)

---

## Machine Learning Pipeline

* Data preprocessing
* Feature engineering and selection
* 10-fold cross-validation
* Models:

  * Logistic Regression
  * Random Forest
  * XGBoost
* Evaluation metric: ROC-AUC

---

## Streamlit Dashboard

Run locally:

```bash
streamlit run app/Home.py
```

Dashboard pages:

* Home — Project overview and KPIs
* EDA — Trends, distributions, and volume analysis
* RQ1 — Seasonality analysis
* RQ2 — Trading strategy evaluation
* RQ3 — Market correlation
* RQ4 — Predictive modeling

---

## Project Structure

```
msft-stock-analytics-dashboard/
│
├── app/                # Streamlit dashboard
├── src/                # Data pipeline and modeling
├── data/               # Raw and processed datasets
├── figures/            # Visual outputs
├── reports/            # Technical documentation
├── tests/              # Unit tests
├── notebooks/          # Analysis notebooks
│
├── requirements.txt
└── README.md
```

---

## How to Run

```
git clone https://github.com/your-username/msft-stock-analytics-dashboard.git
cd msft-stock-analytics-dashboard

pip install -r requirements.txt
streamlit run app/Home.py
```

---

## Key Takeaways

* Stock prediction using technical indicators is highly challenging
* Market trends dominate individual stock behavior
* Machine learning does not guarantee predictive edge in finance
* Proper evaluation and validation are critical

---

## Skills Demonstrated

* Data Analysis and EDA
* Statistical Testing
* Feature Engineering
* Machine Learning Modeling
* Model Evaluation (ROC-AUC, cross-validation)
* Data Visualization
* Dashboard Development (Streamlit)
* Clean project architecture

---

## Future Improvements

* Incorporate macroeconomic indicators
* Explore deep learning models (LSTM)
* Expand feature engineering
* Deploy to cloud platforms (GCP or AWS)

---

## Author

Roberto Alberto San Miguel
Master of Data Analytics – Niagara Falls University

---

If you want, I can next:

* tailor this README for a specific job posting
* or make a stronger “impact/results” section recruiters love
