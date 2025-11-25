import pandas as pd
from src.indicators import compute_basic_indicators, compute_returns


def test_basic_indicators_columns():
    # create a simple increasing Close series
    dates = pd.date_range("2020-01-01", periods=50)
    df = pd.DataFrame({"Close": range(50)}, index=dates)
    out = compute_basic_indicators(df)
    for col in ["SMA_20", "SMA_50", "EMA_20", "RSI_14", "MACD", "MACD_SIGNAL"]:
        assert col in out.columns


def test_compute_returns():
    dates = pd.date_range("2020-01-01", periods=3)
    df = pd.DataFrame({"Close": [100, 110, 121]}, index=dates)
    out = compute_returns(df)
    # percentage returns: 10%, ~10%.
    assert round(out["Return"].iloc[1], 6) == 10.0
