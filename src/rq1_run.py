import pandas as pd
from .config import MSFT_ENGINEERED
from .analytics import monthly_anova

def run():
    df = pd.read_csv(MSFT_ENGINEERED, parse_dates=["date"])
    return monthly_anova(df)
