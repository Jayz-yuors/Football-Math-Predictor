"""
train_model.py
==============

Trains one XGBoost model per league (excluding PL which is already trained).
"""

import joblib
from pathlib import Path
import xgboost as xgb

from model.training.build_training_dataset import build_training_dataset


MODEL_DIR = Path("trained_models")
MODEL_DIR.mkdir(exist_ok=True)

# -----------------------------
# TRAIN ONLY NON-PL LEAGUES
# -----------------------------
LEAGUES = {
    "PD": 2025,    # La Liga
    "SA": 2025,    # Serie A
    "BL1": 2025,   # Bundesliga
    "FL1": 2025    # Ligue 1
}


def train_league_model(competition_code: str, season: int):

    print(f"\n🚀 Training model for {competition_code} ({season})")

    df = build_training_dataset(competition_code, season)

    if df is None or df.empty:
        print(f"⚠️ No usable data for {competition_code}. Skipping.")
        return

    DROP_COLS = [
        "target",
        "match_date",
        "competition_code",
        "home_team",
        "away_team"
    ]

    X = df.drop(columns=[c for c in DROP_COLS if c in df.columns])
    y = df["target"]

    # Safety check
    bad_cols = X.select_dtypes(include="object").columns.tolist()
    if bad_cols:
        raise ValueError(
            f"❌ Non-numeric columns in training data: {bad_cols}"
        )

    model = xgb.XGBClassifier(
        n_estimators=500,
        max_depth=6,
        learning_rate=0.04,
        subsample=0.85,
        colsample_bytree=0.85,
        objective="multi:softprob",
        num_class=3,
        eval_metric="mlogloss",
        random_state=42
    )

    model.fit(X, y)

    joblib.dump(
        model,
        MODEL_DIR / f"{competition_code}_model.joblib"
    )

    print(f"✅ Saved trained_models/{competition_code}_model.joblib")


# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":

    for league, season in LEAGUES.items():
        train_league_model(league, season)

    print("\n🎉 Training completed for available leagues")
