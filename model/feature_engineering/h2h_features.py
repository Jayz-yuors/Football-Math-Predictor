"""
HEAD-TO-HEAD (H2H) FEATURES
==========================

Captures historical dominance, draw tendency,
and psychological advantage between two teams.

Design
------
- Keyword-only arguments (MANDATORY)
- Uses historical matches only
- Safe against argument mis-ordering
"""

import pandas as pd

from model.utils.db_loader import load_matches_by_league


def get_h2h_features(
    *,
    competition_code: str,
    season: int,
    home_team: str,
    away_team: str,
    match_date
) -> dict:
    """
    Compute head-to-head features using all matches
    BEFORE the given match_date.
    """

    matches = load_matches_by_league(competition_code)

    # Only past matches
    matches = matches[matches["match_date"] < match_date]

    h2h = matches[
        (
            (matches["home_team"] == home_team) &
            (matches["away_team"] == away_team)
        ) |
        (
            (matches["home_team"] == away_team) &
            (matches["away_team"] == home_team)
        )
    ]

    if h2h.empty:
        return {
            "h2h_matches": 0,
            "h2h_home_wins": 0,
            "h2h_away_wins": 0,
            "h2h_draws": 0,
            "h2h_goal_diff": 0.0,
        }

    home_wins = 0
    away_wins = 0
    draws = 0
    goal_diff = 0

    for _, row in h2h.iterrows():
        hg = row["home_goals"]
        ag = row["away_goals"]

        if row["home_team"] == home_team:
            goal_diff += hg - ag
            if hg > ag:
                home_wins += 1
            elif ag > hg:
                away_wins += 1
            else:
                draws += 1
        else:
            goal_diff += ag - hg
            if ag > hg:
                home_wins += 1
            elif hg > ag:
                away_wins += 1
            else:
                draws += 1

    return {
        "h2h_matches": len(h2h),
        "h2h_home_wins": home_wins,
        "h2h_away_wins": away_wins,
        "h2h_draws": draws,
        "h2h_goal_diff": round(goal_diff / len(h2h), 3),
    }
