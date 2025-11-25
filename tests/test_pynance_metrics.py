import pandas as pd
from src.analysis.pynance_metrics import compute_metrics_with_pynance


def test_pynance_metrics_fallback():
    returns = pd.Series([0.01, -0.005, 0.002])
    res = compute_metrics_with_pynance(returns)
    assert "sharpe" in res and "annual_return" in res
    assert isinstance(res["sharpe"], float)
