"""
helpers.py
==========

Purpose
-------
Reusable utility helpers used across feature engineering,
training, evaluation, and inference layers.

This file contains:
- Date utilities
- Safe math helpers
- Rolling window helpers
- Football-specific helpers (home/away flags, result encoding)

NO DATABASE ACCESS HERE
"""

import numpy as np
import pandas as pd


# -------------------------
# DATE & TIME HELPERS
# -------------------------

def to_datetime(df, col):
    """Safely convert column to datetime."""
    df[col] = pd.to_datetime(df[col], errors="coerce")
    return df


# -------------------------
# SAFE MATH
# -------------------------

def safe_divide(a, b, default=0.0):
    """Avoid ZeroDivision errors."""
    if b == 0:
        return default
    return a / b


# -------------------------
# FOOTBALL RESULT HELPERS
# -------------------------

def encode_result(home_goals, away_goals):
    """
    Encode match result:
    1  = Home win
    0  = Draw
    -1 = Away win
    """
    if home_goals > away_goals:
        return 1
    elif home_goals < away_goals:
        return -1
    return 0


def is_home(team, home_team):
    """Check if team is playing at home."""
    return team == home_team


# -------------------------
# ROLLING WINDOW HELPERS
# -------------------------

def rolling_mean(series, window):
    """Safe rolling mean with min periods."""
    return series.rolling(window=window, min_periods=1).mean()


def rolling_sum(series, window):
    """Safe rolling sum with min periods."""
    return series.rolling(window=window, min_periods=1).sum()


# -------------------------
# FIXTURE HELPERS
# -------------------------

def upcoming_fixtures(df):
    """Filter upcoming (unplayed) fixtures."""
    return df[df["status"] == "SCHEDULED"]


def completed_fixtures(df):
    """Filter completed fixtures."""
    return df[df["status"] == "FINISHED"]
