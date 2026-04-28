from .data_cleaning import load_stock_csv, clean_stock_data
from .feature_engineering import add_technical_features
from .analytics import msft_qqq_correlation
from .config import MSFT_RAW, QQQ_RAW

def run():
    msft = add_technical_features(clean_stock_data(load_stock_csv(MSFT_RAW)))
    qqq = clean_stock_data(load_stock_csv(QQQ_RAW))
    return msft_qqq_correlation(msft, qqq)
