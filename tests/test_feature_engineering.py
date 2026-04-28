import pandas as pd
from src.feature_engineering import add_technical_features

def test_add_features():
    df = pd.DataFrame({'date':pd.date_range('2024-01-01',periods=250),'open':range(250),'high':range(1,251),'low':range(250),'close':range(1,251),'volume':[100]*250})
    out = add_technical_features(df)
    assert 'target' in out.columns and 'rsi_14' in out.columns
