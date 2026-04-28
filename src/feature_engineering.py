import numpy as np

def add_technical_features(df):
    out = df.copy().sort_values('date')
    out['daily_return'] = out['close'].pct_change()
    for w in [5,10,20,50,200]:
        out[f'ma_{w}'] = out['close'].rolling(w).mean()
    for w in [5,10,20]:
        out[f'std_{w}'] = out['daily_return'].rolling(w).std()
    out['momentum_3'] = out['close'] - out['close'].shift(3)
    out['momentum_7'] = out['close'] - out['close'].shift(7)
    out['rolling_return_3'] = out['close'].pct_change(3)
    out['rolling_return_7'] = out['close'].pct_change(7)
    delta = out['close'].diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()
    rs = gain / loss.replace(0, np.nan)
    out['rsi_14'] = 100 - (100 / (1 + rs))
    ema12 = out['close'].ewm(span=12, adjust=False).mean()
    ema26 = out['close'].ewm(span=26, adjust=False).mean()
    out['macd'] = ema12 - ema26
    out['macd_signal'] = out['macd'].ewm(span=9, adjust=False).mean()
    out['bollinger_width'] = 4 * out['std_20']
    out['volume_change'] = out['volume'].pct_change()
    out['volume_ma_5'] = out['volume'].rolling(5).mean()
    out['price_gap'] = out['open'] - out['close'].shift(1)
    out['close_to_ma50'] = out['close'] / out['ma_50']
    out['close_to_ma200'] = out['close'] / out['ma_200']
    out['ma_gap_5_20'] = out['ma_5'] - out['ma_20']
    out['close_to_range'] = (out['close'] - out['low']) / (out['high'] - out['low']).replace(0, np.nan)
    out['rolling_max_10'] = out['close'].rolling(10).max()
    out['rolling_min_10'] = out['close'].rolling(10).min()
    out['volatility_regime'] = (out['std_10'] > out['std_10'].mean()).astype(int)
    out['rsi_volatility_interaction'] = out['rsi_14'] * out['std_10']
    out['weekday'] = out['date'].dt.weekday
    out['month'] = out['date'].dt.month
    out['day'] = out['date'].dt.day
    out['target'] = (out['close'].shift(-1) > out['close']).astype(int)
    return out
