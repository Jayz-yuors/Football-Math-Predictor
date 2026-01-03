"""
calibration.py
--------------

Evaluate how well predicted probabilities reflect reality.
"""

import pandas as pd
import numpy as np


def calibration_table(y_true, y_proba, class_index, bins=10):
    """
    Reliability table for a single outcome class.
    """

    probs = y_proba[:, class_index]
    df = pd.DataFrame({
        "prob": probs,
        "actual": (y_true == class_index).astype(int)
    })

    df["bin"] = pd.cut(df["prob"], bins=bins)

    summary = df.groupby("bin").agg(
        mean_predicted_prob=("prob", "mean"),
        actual_rate=("actual", "mean"),
        samples=("actual", "count")
    )

    return summary.reset_index()


def expected_calibration_error(y_true, y_proba, bins=10):
    """
    Multiclass Expected Calibration Error (ECE)
    """

    ece = 0
    n = len(y_true)

    for c in range(3):
        probs = y_proba[:, c]
        actual = (y_true == c).astype(int)

        df = pd.DataFrame({"prob": probs, "actual": actual})
        df["bin"] = pd.cut(df["prob"], bins=bins)

        for _, g in df.groupby("bin"):
            if len(g) == 0:
                continue
            acc = g["actual"].mean()
            conf = g["prob"].mean()
            ece += (len(g) / n) * abs(acc - conf)

    return ece
