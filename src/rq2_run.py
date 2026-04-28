import pandas as pd
from .config import MSFT_ENGINEERED
from .analytics import create_crossover_events

def run():
    df = pd.read_csv(MSFT_ENGINEERED, parse_dates=["date"])
    return create_crossover_events(df)
