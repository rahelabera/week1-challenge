import pandas as pd
from src.analysis.correlation import daily_average_sentiment, compute_sentiment_return_correlation


def test_daily_average_sentiment_simple():
    data = pd.DataFrame({
        "headline": ["good news", "bad news", "neutral"],
        "date": ["2020-01-01", "2020-01-01", "2020-01-02"],
    })
    agg = daily_average_sentiment(data)
    assert "2020-01-01" in agg.index.astype(str).tolist()
    assert "2020-01-02" in agg.index.astype(str).tolist()


def test_compute_sentiment_return_correlation_trivial():
    # generate a simple news sentiment and matching returns
    news = pd.DataFrame({
        "headline": ["good", "bad", "good"],
        "date": ["2020-01-02", "2020-01-03", "2020-01-04"],
    })
    stock = pd.DataFrame(
        {"Close": [100, 102, 104, 106, 101]},
        index=pd.date_range("2020-01-01", periods=5),
    )
    r, n = compute_sentiment_return_correlation(news, stock)
    # Expect a valid number and non-negative aligned days
    assert isinstance(r, float)
    assert isinstance(n, int)
