from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
FIGURES_DIR = PROJECT_ROOT / "figures"
MSFT_RAW = RAW_DATA_DIR / "MSFT.csv"
QQQ_RAW = RAW_DATA_DIR / "QQQ.csv"
MSFT_ENGINEERED = PROCESSED_DATA_DIR / "msft_engineered_features.csv"
FINAL_FEATURES = ['ma_5','std_5','bollinger_width','volatility_regime','volume_change','daily_return','rolling_return_3','momentum_3','momentum_7','rsi_14','rsi_volatility_interaction','price_gap','close_to_ma50','ma_gap_5_20','close_to_range','weekday','month','day','rolling_max_10']
