"""Lightweight wrapper to compute financial metrics using PyNance if available.
"""
from typing import Dict
import numpy as np
import pandas as pd


def compute_metrics_with_pynance(returns: pd.Series) -> Dict[str, float]:
    """Compute metrics (sharpe, annual_return) using PyNance if installed.

    returns: daily returns in decimal (e.g., 0.01 = 1%)
    """
    try:
        import pynance as pn  # type: ignore

        # PyNance might expect a time series object; we'll try a direct call
        metrics = pn.metrics.summary(returns)
        return {k: float(v) for k, v in metrics.items()}
    except Exception:
        # fallback manual calculations
        mean_daily = returns.mean()
        std_daily = returns.std(ddof=0) if returns.std(ddof=0) != 0 else 1e-9
        sharpe = (mean_daily / std_daily) * np.sqrt(252)
        annual_return = ((1 + mean_daily) ** 252) - 1
        return {"sharpe": float(sharpe), "annual_return": float(annual_return)}
