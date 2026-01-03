"""
build_training_dataset.py
=========================

Builds a supervised training dataset by looping over
historical matches and generating features per match.
"""

import pandas as pd

from model.utils.db_loader import load_matches_by_league_season
from model.feature_engineering.match_feature_builder import build_match_features


def build_training_dataset(
    competition_code: str,
    season: int
) -> pd.DataFrame:

    matches = load_matches_by_league_season(
        competition_code=competition_code,
        season=season
    )

    if matches.empty:
        raise ValueError(
            f"No matches found for {competition_code} {season}"
        )

    rows = []

    for _, m in matches.iterrows():

        # 🔒 Skip incomplete matches
        if pd.isna(m["home_goals"]) or pd.isna(m["away_goals"]):
            continue

        feature_row = build_match_features(
            competition_code=competition_code,
            season=season,
            home_team=m["home_team"],
            away_team=m["away_team"],
            match_date=m["match_date"]
        )

        # 🔒 Feature builder failed
        if not isinstance(feature_row, dict) or not feature_row:
            continue

        # 🎯 Target encoding
        if m["home_goals"] > m["away_goals"]:
            target = 2   # HOME WIN
        elif m["home_goals"] < m["away_goals"]:
            target = 0   # AWAY WIN
        else:
            target = 1   # DRAW

        feature_row["target"] = target
        feature_row["match_date"] = m["match_date"]

        rows.append(feature_row)

    df = pd.DataFrame(rows)

    if df.empty:
        raise ValueError(
            "Training dataset is empty after feature generation"
        )

    # 🔥 FINAL SAFETY — ensure no nested objects slipped in
    for col in df.columns:
        if df[col].apply(lambda x: isinstance(x, (dict, list, tuple))).any():
            raise ValueError(
                f"Invalid nested data found in column: {col}"
            )

    return df
