"""
FORM FEATURES
=============

Builds rolling form-based features for both teams in a match.

Concept of form:
- Recent performance matters more than old matches
- Home and away performance differ
- Goals scored & conceded indicate momentum

All computations are:
- League-specific
- Time-aware (no future leakage)
"""

import pandas as pd
from model.utils.db_loader import load_matches,load_matches_by_league_season

WINDOW = 5  # last N matches


def _compute_team_form(matches_df: pd.DataFrame, team: str, match_date):
    """
    Compute rolling form for a single team before a given date.
    """

    # Ensure match_date comparison is safe
    matches_df["match_date"] = pd.to_datetime(matches_df["match_date"])

    team_matches = matches_df[
        (
            (matches_df["home_team"] == team) |
            (matches_df["away_team"] == team)
        ) &
        (matches_df["match_date"] < pd.to_datetime(match_date))
    ].sort_values("match_date", ascending=False).head(WINDOW)

    if team_matches.empty:
        return {
            "matches_played": 0,
            "points": 0,
            "goals_scored": 0,
            "goals_conceded": 0
        }

    points = 0
    goals_scored = 0
    goals_conceded = 0

    for _, m in team_matches.iterrows():
        if m["home_team"] == team:
            gs = m["home_goals"]
            gc = m["away_goals"]
        else:
            gs = m["away_goals"]
            gc = m["home_goals"]

        goals_scored += gs
        goals_conceded += gc

        if gs > gc:
            points += 3
        elif gs == gc:
            points += 1

    return {
        "matches_played": len(team_matches),
        "points": points,
        "goals_scored": goals_scored,
        "goals_conceded": goals_conceded
    }


def get_team_form_features(
    competition_code: str,
    season: int,
    home_team: str,
    away_team: str,
    match_date
):
    """
    Returns rolling form features for both teams.
    """

    # Load historical matches ONCE (DB-backed)
    matches_df = load_matches_by_league_season(
    competition_code=competition_code,
    season=season
    )

    home_form = _compute_team_form(matches_df, home_team, match_date)
    away_form = _compute_team_form(matches_df, away_team, match_date)

    features = {
        # Home form
        "home_form_points": home_form["points"],
        "home_form_goals_scored": home_form["goals_scored"],
        "home_form_goals_conceded": home_form["goals_conceded"],

        # Away form
        "away_form_points": away_form["points"],
        "away_form_goals_scored": away_form["goals_scored"],
        "away_form_goals_conceded": away_form["goals_conceded"],

        # Relative differences
        "form_points_diff": home_form["points"] - away_form["points"],
        "form_goal_diff": (
            (home_form["goals_scored"] - home_form["goals_conceded"]) -
            (away_form["goals_scored"] - away_form["goals_conceded"])
        )
    }

    return features