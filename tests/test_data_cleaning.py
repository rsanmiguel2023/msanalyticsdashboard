import pandas as pd
from src.data_cleaning import clean_stock_data

def test_clean_stock_data():
    df = pd.DataFrame({'date':['2024-01-02','2024-01-01'],'open':[2,1],'high':[2,1],'low':[2,1],'close':[2,1],'volume':[20,10]})
    out = clean_stock_data(df)
    assert out.date.is_monotonic_increasing
