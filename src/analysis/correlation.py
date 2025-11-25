"""Helpers to compute correlation between news sentiment and stock returns.
"""
from typing import Tuple
from pathlib import Path

import numpy as np
import pandas as pd

from ..sentiment import get_sentiment_fn
from ..data.loader import load_stock_csv, load_news_csv
from ..indicators import compute_returns


def daily_average_sentiment(news_df: pd.DataFrame) -> pd.DataFrame:
    """Compute average daily sentiment for a news DataFrame.

    Expects a `date` column and `headline`. Returns DataFrame with index=Date and
    a `sentiment` float column.
    """
    scorer = get_sentiment_fn()

    def score_row(text):
        try:
            return float(scorer(str(text)))
        except Exception:
            return 0.0

    news_df = news_df.copy()
    news_df["date_dt"] = pd.to_datetime(news_df["date"]).dt.floor("D")
    news_df["_sentiment"] = news_df["headline"].apply(score_row)
    grouped = news_df.groupby("date_dt")["_sentiment"].mean().rename("sentiment")
    return grouped.to_frame()


def compute_sentiment_return_correlation(news_df: pd.DataFrame, stock_df: pd.DataFrame) -> Tuple[float, int]:
    """Compute Pearson correlation between average daily sentiment and daily returns.

    Returns (r, n) where r is Pearson correlation, n is number of aligned days.
    """
    sentiment_df = daily_average_sentiment(news_df)
    returns_df = compute_returns(stock_df)[["Return"]].copy()
    returns_df.index = pd.to_datetime(returns_df.index).floor("D")
    merged = sentiment_df.join(returns_df, how="inner")
    merged = merged.dropna()
    if len(merged) < 2:
        return float("nan"), 0
    r = np.corrcoef(merged["sentiment"].values, merged["Return"].values)[0, 1]
    return float(r), int(len(merged))


def correlation_report(news_path: Path = None, symbol: str = "AAPL") -> dict:
    news_df = load_news_csv(news_path)
    stock_df = load_stock_csv(symbol)
    r, n = compute_sentiment_return_correlation(news_df, stock_df)
    return {
        "symbol": symbol,
        "correlation": r,
        "aligned_days": n,
    }
