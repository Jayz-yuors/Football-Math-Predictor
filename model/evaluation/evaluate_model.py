"""
evaluate_model.py
=================

Single entry point for evaluating trained models.

This file:
- Loads test data
- Runs all evaluation modules
- Prints structured results
"""

import numpy as np
import pandas as pd

from evaluation.metrics import classification_metrics, probability_metrics
from evaluation.calibration import expected_calibration_error
from evaluation.baseline import home_bias_baseline
from evaluation.diagnostics import confidence_mistakes


def evaluate(y_true, y_pred, y_proba):
    print("\n=== CLASSIFICATION METRICS ===")
    print(classification_metrics(y_true, y_pred))

    print("\n=== PROBABILITY METRICS ===")
    print(probability_metrics(y_true, y_proba))

    print("\n=== CALIBRATION ===")
    print("ECE:", expected_calibration_error(y_true, y_proba))

    print("\n=== CONFIDENCE ERRORS ===")
    print(confidence_mistakes(y_true, y_proba))


def evaluate_against_baseline(y_true, y_proba):
    baseline = home_bias_baseline(len(y_true))

    print("\n=== BASELINE COMPARISON ===")
    print("Model LogLoss:",
          probability_metrics(y_true, y_proba)["log_loss"])
    print("Baseline LogLoss:",
          probability_metrics(y_true, baseline)["log_loss"])
