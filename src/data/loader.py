"""Data loading utilities for stocks and news.

Functions in this module load CSV data from `data/` and return pandas
DataFrames with sensible parsing and column names.
"""
from pathlib import Path
from typing import Optional

import pandas as pd


def load_stock_csv(symbol: str, data_dir: Optional[Path] = None) -> pd.DataFrame:
    """Load a stock CSV for a given symbol.

    Expects files like `data/AAPL.csv` with Date, Open, High, Low, Close, Volume.
    Returns a DataFrame indexed by a parsed `Date` column.
    """
    data_dir = Path(data_dir or Path(__file__).parents[2] / "data")
    path = data_dir / f"{symbol}.csv"
    if not path.exists():
        raise FileNotFoundError(f"Stock CSV not found: {path}")
    df = pd.read_csv(path, parse_dates=["Date"])
    df = df.sort_values("Date").reset_index(drop=True)
    df["Date"] = pd.to_datetime(df["Date"])
    df.set_index("Date", inplace=True)
    # Ensure required columns exist (some CSVs may vary)
    expected = ["Open", "High", "Low", "Close", "Volume"]
    for col in expected:
        if col not in df.columns:
            # Some datasets use lowercase or different column names
            if col.lower() in df.columns:
                df[col] = df[col.lower()]
            else:
                raise KeyError(f"Missing column {col} in {path}")
    return df


def load_news_csv(path: Optional[Path] = None) -> pd.DataFrame:
    """Load the news CSV and normalize key fields.

    Returns a DataFrame with columns: ['headline', 'url', 'publisher', 'date', 'stock']
    and `date` parsed as datetime without timezone for easier alignment.
    """
    path = Path(path or Path(__file__).parents[2] / "data" / "raw_analyst_ratings.csv")
    if not path.exists():
        raise FileNotFoundError(f"News CSV not found: {path}")
    df = pd.read_csv(path, dtype=str)
    # Normalize column names (strip whitespace)
    df.columns = [c.strip() for c in df.columns]
    # Parse date safely
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    # Clean headline
    if "headline" in df.columns:
        df["headline"] = df["headline"].astype(str).str.strip()
    # If publisher contains email addresses, extract domain
    if "publisher" in df.columns:
        df["publisher_clean"] = (
            df["publisher"].str.extract(r"([A-Za-z0-9_.+-]+@[A-Za-z0-9-]+\.[A-Za-z0-9-.]+)")
            .fillna("")
        )
        # fallback: just publisher name
        df["publisher_clean"] = df.apply(
            lambda row: row.publisher.split("@")[-1] if "@" in str(row.publisher) else str(row.publisher),
            axis=1,
        )
    return df
