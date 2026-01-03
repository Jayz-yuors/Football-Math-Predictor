"""
model_loader.py
===============

Purpose
-------
Loads trained ML models for inference.

Design
------
- One model per league
- Read-only
- Centralized loading logic
"""

import joblib
from pathlib import Path

# Base path: project_root/models/
BASE_MODEL_DIR = Path(__file__).resolve().parents[2] / "trained_models"


def load_trained_model(competition_code: str):
    """
    Load trained model for a given league.

    Example:
    --------
    competition_code = "PL"
    loads:
    trained_models/PL_model.joblib
    """

    model_path = BASE_MODEL_DIR / f"{competition_code}_model.joblib"

    if not model_path.exists():
        raise FileNotFoundError(
            f"❌ Trained model not found for {competition_code}: {model_path}"
        )

    return joblib.load(model_path)
