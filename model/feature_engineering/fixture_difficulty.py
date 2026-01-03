"""
FIXTURE DIFFICULTY FEATURES
===========================

Estimates how difficult a team's UPCOMING fixtures are
after the current match.

Purpose
-------
- Measures schedule pressure
- Used for strategic & incentive modeling
- Harder future fixtures → higher importance of current match

Design
------
- Keyword-only arguments (MANDATORY)
- Uses fixtures_current_season table
- No ML logic here, only deterministic features
"""

import pandas as pd
from datetime import date

from model.utils.db_loader import load_fixtures_by_league


def get_fixture_difficulty_features(
    *,
    competition_code: str,
    season: int,
    home_team: str,
    away_team: str,
    match_date: date,
    window: int = 5
) -> dict:
    """
    Compute future fixture difficulty for both teams.

    window:
        Number of upcoming matches to consider
    """

    fixtures = load_fixtures_by_league(competition_code)

    # Only future fixtures
    fixtures = fixtures[
        (fixtures["match_date"] > match_date) &
        (fixtures["status"] == "SCHEDULED")
    ]

    def team_difficulty(team: str) -> float:
        team_games = fixtures[
            (fixtures["home_team"] == team) |
            (fixtures["away_team"] == team)
        ].sort_values("match_date").head(window)

        if team_games.empty:
            return 0.0

        # Simple heuristic:
        # Away matches are harder than home matches
        difficulty = 0.0
        for _, row in team_games.iterrows():
            if row["away_team"] == team:
                difficulty += 1.2
            else:
                difficulty += 1.0

        return round(difficulty / len(team_games), 3)

    return {
        "home_future_fixture_difficulty": team_difficulty(home_team),
        "away_future_fixture_difficulty": team_difficulty(away_team),
    }
