"""Compute sentiment vs returns correlation for a given symbol and news file.

Usage: python -m scripts.analyze_sentiment_returns --symbol AAPL --news data/raw_analyst_ratings.csv
"""
import argparse
from pathlib import Path
import json

from src.data.loader import load_news_csv
from src.data.loader import load_stock_csv
from src.analysis.correlation import compute_sentiment_return_correlation


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", required=True)
    parser.add_argument("--news", default=None)
    args = parser.parse_args()
    news_df = load_news_csv(args.news)
    stock_df = load_stock_csv(args.symbol)
    r, n = compute_sentiment_return_correlation(news_df, stock_df)
    out = {"symbol": args.symbol, "correlation": r, "aligned_days": n}
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
