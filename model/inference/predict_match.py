"""
predict_match.py
================

Perform live match prediction for a given fixture.

- No DB loading
- No feature logic
- Numeric-only XGBoost input
"""

import pandas as pd

from model.feature_engineering.match_feature_builder import build_match_features
from model.inference.model_loader import load_trained_model


# -----------------------------
# NON-FEATURE COLUMNS
# -----------------------------
NON_FEATURE_COLUMNS = {
    "competition_code",
    "season",
    "home_team",
    "away_team",
    "match_date"
}


def predict_match(
    competition_code: str,
    home_team: str,
    away_team: str,
    season: int,
    match_date
):
    # -----------------------------
    # BUILD FEATURES
    # -----------------------------
    feature_row = build_match_features(
        competition_code=competition_code,
        season=season,
        home_team=home_team,
        away_team=away_team,
        match_date=match_date
    )

    if not feature_row:
        raise ValueError("❌ Feature construction failed")

    X = pd.DataFrame([feature_row])

    # -----------------------------
    # DROP IDENTIFIERS
    # -----------------------------
    X = X.drop(
        columns=[c for c in X.columns if c in NON_FEATURE_COLUMNS],
        errors="ignore"
    )

    # -----------------------------
    # NUMERIC SAFETY CHECK
    # -----------------------------
    bad_cols = X.select_dtypes(include=["object"]).columns.tolist()
    if bad_cols:
        raise ValueError(f"❌ Non-numeric columns passed to model: {bad_cols}")

    # -----------------------------
    # LOAD MODEL
    # -----------------------------
    model = load_trained_model(competition_code)

    # -----------------------------
    # FEATURE ALIGNMENT
    # -----------------------------
    expected_features = model.get_booster().feature_names
    X = X[expected_features]

    # -----------------------------
    # PREDICT
    # -----------------------------
    proba = model.predict_proba(X)[0]

    return {
        "home_win": round(float(proba[2]), 3),
        "draw": round(float(proba[1]), 3),
        "away_win": round(float(proba[0]), 3),
    }


# -----------------------------
# CLI TEST
# -----------------------------
if __name__ == "__main__":
    result = predict_match(
        competition_code="PL",
        home_team="Man United",
        away_team="Crystal Palace",
        season=2025,
        match_date="2026-01-01"
    )

    print("🔮 Prediction:", result)
