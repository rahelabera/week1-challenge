"""Simple indicator helpers.

These functions use pandas and pandas_ta if available. They are intentionally
lightweight so they can be imported in environments that don't have TA-Lib
installed during early development. Unit tests should import these modules
but won't execute heavy computations.
"""
from typing import Optional, Iterable
import pandas as pd


def safe_moving_average(series, window: int = 20):
    """Return a simple moving average for a sequence-like object.

    If pandas is available and series is a pandas Series this will return a
    pandas Series; otherwise it returns a list of floats with None for the
    first (window-1) entries.
    """
    try:
        import pandas as pd

        if isinstance(series, pd.Series):
            return series.rolling(window=window, min_periods=1).mean()
    except Exception:
        pass

    # Fallback: compute simple moving average on iterables
    vals = list(series)
    out = []
    for i in range(len(vals)):
        start = max(0, i - window + 1)
        window_vals = vals[start : i + 1]
        try:
            out.append(sum(window_vals) / len(window_vals))
        except Exception:
            out.append(None)
    return out


def indicator_summary():
    """Return a short string indicating which backends are available."""
    backends = []
    try:
        import talib  # type: ignore

        backends.append("TA-Lib")
    except Exception:
        pass
    try:
        import pandas_ta  # type: ignore

        backends.append("pandas_ta")
    except Exception:
        pass
    return f"available: {', '.join(backends) if backends else 'none'}"


def compute_basic_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Compute a set of basic technical indicators on the dataframe.

    Operates in-place or returns a new DataFrame with columns added:
    - SMA_20, SMA_50
    - EMA_20
    - RSI_14
    - MACD, MACD_SIGNAL
    """
    if "Close" not in df.columns:
        raise KeyError("DataFrame must have a 'Close' column")
    out = df.copy()
    # Attempt to use pandas_ta if available
    use_pandas_ta = False
    try:
        import pandas_ta as pta  # type: ignore

        use_pandas_ta = True
    except Exception:
        use_pandas_ta = False

    if use_pandas_ta:
        out["SMA_20"] = pta.sma(out["Close"], length=20)
        out["SMA_50"] = pta.sma(out["Close"], length=50)
        out["EMA_20"] = pta.ema(out["Close"], length=20)
        out["RSI_14"] = pta.rsi(out["Close"], length=14)
        macd = pta.macd(out["Close"], fast=12, slow=26, signal=9)
        # pandas_ta returns a DataFrame when asking for macd
        if isinstance(macd, pd.DataFrame):
            out["MACD"] = macd["MACD_12_26_9"]
            out["MACD_SIGNAL"] = macd["MACDs_12_26_9"]
        else:
            out["MACD"] = macd
    else:
        # fallback to pandas rolling and TA-Lib if installed
        out["SMA_20"] = out["Close"].rolling(window=20, min_periods=1).mean()
        out["SMA_50"] = out["Close"].rolling(window=50, min_periods=1).mean()
        out["EMA_20"] = out["Close"].ewm(span=20, adjust=False).mean()
        # RSI calculation
        try:
            import talib  # type: ignore

            out["RSI_14"] = talib.RSI(out["Close"].values, timeperiod=14)
        except Exception:
            # simple RSI implementation
            delta = out["Close"].diff()
            up = delta.clip(lower=0)
            down = -1 * delta.clip(upper=0)
            ma_up = up.rolling(window=14, min_periods=1).mean()
            ma_down = down.rolling(window=14, min_periods=1).mean()
            rs = ma_up / (ma_down.replace(0, 1e-9))
            out["RSI_14"] = 100 - (100 / (1 + rs))
        # MACD calculation
        try:
            import talib  # type: ignore

            macd_val, macd_sig, macd_hist = talib.MACD(out["Close"].values, fastperiod=12, slowperiod=26, signalperiod=9)
            out["MACD"] = macd_val
            out["MACD_SIGNAL"] = macd_sig
        except Exception:
            ema_fast = out["Close"].ewm(span=12, adjust=False).mean()
            ema_slow = out["Close"].ewm(span=26, adjust=False).mean()
            out["MACD"] = ema_fast - ema_slow
            out["MACD_SIGNAL"] = out["MACD"].ewm(span=9, adjust=False).mean()

    return out


def compute_returns(df: pd.DataFrame, column: str = "Close") -> pd.DataFrame:
    """Compute daily percentage returns for the `column` provided.

    Returns a DataFrame with an added `Return` column.
    """
    out = df.copy()
    out["Return"] = out[column].pct_change() * 100
    return out

