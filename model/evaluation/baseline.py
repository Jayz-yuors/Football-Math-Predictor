"""
baseline.py
-----------

Naive football baselines for comparison.
"""

import numpy as np


def home_bias_baseline(n_samples):
    """
    Always predict HOME WIN with fixed probabilities
    """
    probs = np.zeros((n_samples, 3))
    probs[:, 2] = 0.45  # home
    probs[:, 1] = 0.25  # draw
    probs[:, 0] = 0.30  # away
    return probs


def uniform_baseline(n_samples):
    return np.ones((n_samples, 3)) / 3
