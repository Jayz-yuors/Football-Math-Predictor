"""
calibrate_model.py
==================

Optional probability calibration.
"""

import joblib
from sklearn.calibration import CalibratedClassifierCV

from model.training.build_training_dataset import build_training_dataset


def calibrate_model(competition_code: str, season: int):

    df = build_training_dataset(competition_code, season)
    X = df.drop(columns=["target", "match_date"])
    y = df["target"]

    base_model = joblib.load(
        f"trained_models/{competition_code}_model.joblib"
    )

    calibrated = CalibratedClassifierCV(
        base_model,
        method="isotonic",
        cv=5
    )

    calibrated.fit(X, y)

    joblib.dump(
        calibrated,
        f"trained_models/{competition_code}_model_calibrated.joblib"
    )

if __name__ == "__main__":

    LEAGUES = {
        "PL": 2025,
        "PD": 2025,
        "SA": 2025,
        "BL1": 2025,
        "FL1": 2025
    }

    for league, season in LEAGUES.items():
        calibrate_model(league, season)
