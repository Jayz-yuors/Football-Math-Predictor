"""
diagnostics.py
--------------

Football-specific diagnostics.
"""

import pandas as pd
import numpy as np


def home_away_accuracy(df):
    """
    df must contain:
    - y_true
    - y_pred
    - home_team
    """

    home_games = df[df["y_true"] == 2]
    away_games = df[df["y_true"] == 0]

    return {
        "home_accuracy": (home_games["y_pred"] == 2).mean(),
        "away_accuracy": (away_games["y_pred"] == 0).mean()
    }


def confidence_mistakes(y_true, y_proba, threshold=0.7):
    """
    Count high-confidence wrong predictions
    """
    preds = y_proba.argmax(axis=1)
    conf = y_proba.max(axis=1)

    wrong = (preds != y_true) & (conf >= threshold)

    return {
        "high_confidence_errors": wrong.sum(),
        "error_rate": wrong.mean()
    }
