import pandas as pd
from .config import PROCESSED_DATA_DIR

def run():
    return pd.read_csv(PROCESSED_DATA_DIR / "rq4_model_results.csv")
