"""Small CLI for computing indicators for a given symbol.

Usage: python -m scripts.compute_indicators --symbol AAPL
"""
import argparse
from pathlib import Path

import pandas as pd

from src.data.loader import load_stock_csv
from src.indicators import compute_basic_indicators


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", required=True, help="Ticker symbol (filename without .csv)")
    parser.add_argument("--out", default=None, help="Output CSV path")
    args = parser.parse_args()
    out_dir = Path(args.out or Path(__file__).parents[2] / "data" / "processed")
    out_dir.mkdir(parents=True, exist_ok=True)
    df = load_stock_csv(args.symbol)
    df_ind = compute_basic_indicators(df)
    out_path = Path(out_dir) / f"{args.symbol}_indicators.csv"
    df_ind.to_csv(out_path, index=True)
    print(f"Wrote indicators to {out_path}")


if __name__ == "__main__":
    main()
