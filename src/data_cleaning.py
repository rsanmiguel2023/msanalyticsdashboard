import pandas as pd
REQUIRED_COLUMNS = ['date','open','high','low','close','volume']

def load_stock_csv(path):
    df = pd.read_csv(path)
    df.columns = [c.strip().lower() for c in df.columns]
    missing = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    return df

def clean_stock_data(df):
    out = df.copy()
    out['date'] = pd.to_datetime(out['date'], errors='coerce')
    for col in ['open','high','low','close','volume']:
        out[col] = pd.to_numeric(out[col], errors='coerce')
    return out.dropna(subset=REQUIRED_COLUMNS).sort_values('date').drop_duplicates('date').reset_index(drop=True)
