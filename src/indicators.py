"""Simple indicator helpers.

These functions use pandas and pandas_ta if available. They are intentionally
lightweight so they can be imported in environments that don't have TA-Lib
installed during early development. Unit tests should import these modules
but won't execute heavy computations.
"""
from typing import Optional


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
