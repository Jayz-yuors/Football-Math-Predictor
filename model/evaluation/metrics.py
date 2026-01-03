"""
metrics.py
----------

Core evaluation metrics for match prediction models.
Focuses on probability-aware metrics.
"""

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    log_loss,
    brier_score_loss,
    roc_auc_score
)


def classification_metrics(y_true, y_pred):
    return {
        "accuracy": accuracy_score(y_true, y_pred)
    }


def probability_metrics(y_true, y_proba):
    """
    y_proba shape: (n_samples, 3)
    classes: [away_win, draw, home_win]
    """

    metrics = {}

    metrics["log_loss"] = log_loss(y_true, y_proba)

    # Brier score (multiclass mean)
    brier = 0
    for i in range(3):
        brier += brier_score_loss(
            (y_true == i).astype(int),
            y_proba[:, i]
        )
    metrics["brier_score"] = brier / 3

    try:
        metrics["roc_auc"] = roc_auc_score(
            y_true, y_proba, multi_class="ovr"
        )
    except Exception:
        metrics["roc_auc"] = None

    return metrics
