"""
MATCH FEATURE BUILDER
=====================

Central orchestration layer that builds a SINGLE
model-ready feature dictionary for one football match.

Responsibilities
----------------
- Acts as the ONLY entry point for feature construction
- Delegates logic to individual feature modules
- Uses keyword-only calls to prevent argument order bugs
- Returns a flat, model-ready feature dict

IMPORTANT
---------
- No database access here
- No positional arguments in feature calls
"""

from typing import Dict
from datetime import date

from model.feature_engineering.form_features import get_team_form_features
from model.feature_engineering.table_features import get_table_features
from model.feature_engineering.player_strength import get_player_strength_features
from model.feature_engineering.incentive_features import get_incentive_features
from model.feature_engineering.fixture_difficulty import get_fixture_difficulty_features
from model.feature_engineering.h2h_features import get_h2h_features


def build_match_features(
    *,
    competition_code: str,
    season: int,
    home_team: str,
    away_team: str,
    match_date: date
) -> Dict:
    """
    Build a complete feature dictionary for one football match.
    """

    features = {}

    # -------------------------------------------------
    # BASIC CONTEXT
    # -------------------------------------------------
    features["competition_code"] = competition_code
    features["home_team"] = home_team
    features["away_team"] = away_team
    features["home_advantage"] = 1

    # -------------------------------------------------
    # RECENT TEAM FORM
    # -------------------------------------------------
    features.update(
        get_team_form_features(
            competition_code=competition_code,
            season=season,
            home_team=home_team,
            away_team=away_team,
            match_date=match_date
        )
    )

    # -------------------------------------------------
    # PLAYER / SQUAD STRENGTH
    # -------------------------------------------------
    features.update(
        get_player_strength_features(
            competition_code=competition_code,
            season=season,
            home_team=home_team,
            away_team=away_team
        )
    )

    # -------------------------------------------------
    # LEAGUE TABLE CONTEXT
    # -------------------------------------------------
    features.update(
        get_table_features(
            competition_code=competition_code,
            season=season,
            home_team=home_team,
            away_team=away_team,
            match_date=match_date
        )
    )

    # -------------------------------------------------
    # STRATEGIC INCENTIVE (TOP 4 / RELEGATION / TARGETS)
    # -------------------------------------------------
    features.update(
        get_incentive_features(
            competition_code=competition_code,
            season=season,
            home_team=home_team,
            away_team=away_team,
            match_date=match_date
        )
    )

    # -------------------------------------------------
    # FUTURE FIXTURE DIFFICULTY
    # -------------------------------------------------
    features.update(
        get_fixture_difficulty_features(
            competition_code=competition_code,
            season=season,
            home_team=home_team,
            away_team=away_team,
            match_date=match_date
        )
    )

    # -------------------------------------------------
    # HEAD-TO-HEAD HISTORY
    # -------------------------------------------------
    features.update(
        get_h2h_features(
            competition_code=competition_code,
            season=season,
            home_team=home_team,
            away_team=away_team,
            match_date=match_date
        )
    )

    return features
