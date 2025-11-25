"""Simple sentiment helpers.

This module provides a tiny wrapper around available sentiment tools. It will
attempt to use Vader (from nltk) or TextBlob if installed; otherwise it falls
back to a neutral score of 0.0. The functions are lightweight so they can be
imported safely in CI before heavy deps are installed.
"""
from typing import List, Tuple


def _use_vader():
    try:
        from nltk.sentiment import SentimentIntensityAnalyzer

        sia = SentimentIntensityAnalyzer()

        def f(text: str) -> float:
            return sia.polarity_scores(text)["compound"]

        return f
    except Exception:
        return None


def _use_textblob():
    try:
        from textblob import TextBlob

        def f(text: str) -> float:
            return TextBlob(text).sentiment.polarity # type: ignore

        return f
    except Exception:
        return None


def get_sentiment_fn():
    """Return the best available sentiment scoring function.

    The function returned accepts a single string and returns a float in
    approximately [-1, 1] where negative values indicate negative sentiment.
    """
    for fn in (_use_vader, _use_textblob):
        candidate = fn()
        if candidate is not None:
            return candidate

    # fallback: neutral
    return lambda text: 0.0


def average_daily_sentiment(items: List[Tuple[str, str]]):
    """Compute average sentiment per day.

    items: list of (date_str, text). Returns dict date_str -> average score.
    This is purposely small and robust for early stages.
    """
    scorer = get_sentiment_fn()
    from collections import defaultdict

    agg = defaultdict(list)
    for date, text in items:
        try:
            score = float(scorer(text))
        except Exception:
            score = 0.0
        agg[date].append(score)
    return {d: sum(vals) / len(vals) if vals else 0.0 for d, vals in agg.items()}
