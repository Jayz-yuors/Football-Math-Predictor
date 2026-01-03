"""
STRATEGIC INCENTIVE FEATURES
===========================

Models WHY a team wants to win a match.
Fully defensive & training-safe.
"""

import pandas as pd

from model.utils.league_table import fetch_league_table
from model.utils.db_loader import load_fixtures_current_season


# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def get_target_zone(position: int, total_teams: int) -> str:
    if position <= 4:
        return "TOP4"
    elif position <= total_teams - 4:
        return "MID"
    else:
        return "SURVIVAL"


# --------------------------------------------------
# SINGLE TEAM STRATEGIC FEATURES
# --------------------------------------------------

def get_strategic_incentive_features(
    competition_code: str,
    season: int,
    team_name: str,
    match_date
) -> dict:

    table = fetch_league_table(
        competition_code=competition_code,
        season=season
    )

    if table.empty or "team" not in table.columns:
        return {
            "remaining_matches": 0,
            "points_gap_to_target": 0,
            "target_zone": "UNKNOWN",
            "must_win_match": 0,
            "high_pressure_match": 0
        }

    fixtures = load_fixtures_current_season()

    fixtures = fixtures[
        (fixtures["competition_code"] == competition_code) &
        (fixtures["match_date"] >= match_date)
    ]

    team_row = table[table["team"] == team_name]

    if team_row.empty:
        return {
            "remaining_matches": 0,
            "points_gap_to_target": 0,
            "target_zone": "UNKNOWN",
            "must_win_match": 0,
            "high_pressure_match": 0
        }

    team_row = team_row.iloc[0]

    position = int(team_row["position"])
    points = int(team_row["points"])
    total_teams = len(table)

    target_zone = get_target_zone(position, total_teams)

    remaining_matches = len(
        fixtures[
            (fixtures["home_team"] == team_name) |
            (fixtures["away_team"] == team_name)
        ]
    )

    if target_zone == "TOP4":
        target_points = table.loc[table["position"] == 4, "points"].iloc[0]
        points_gap = target_points - points
    elif target_zone == "SURVIVAL":
        safe_position = total_teams - 3
        target_points = table.loc[
            table["position"] == safe_position, "points"
        ].iloc[0]
        points_gap = points - target_points
    else:
        points_gap = 0

    must_win = int(
        remaining_matches > 0 and
        points_gap > 0 and
        (points_gap / max(remaining_matches, 1)) >= 1.8
    )

    return {
        "remaining_matches": remaining_matches,
        "points_gap_to_target": int(points_gap),
        "target_zone": target_zone,
        "must_win_match": must_win,
        "high_pressure_match": int(points_gap > 0)
    }


# --------------------------------------------------
# BACKWARD-COMPATIBILITY (USED BY TRAINING)
# --------------------------------------------------

def get_incentive_features(
    *,
    home_team,
    away_team,
    competition_code,
    season,
    match_date
):
    table = fetch_league_table(
        competition_code=competition_code,
        season=season,
        as_of_date=match_date
    )

    if table.empty or "team" not in table.columns:
        return {
            "home_incentive": 0,
            "away_incentive": 0,
            "incentive_diff": 0
        }

    def team_row(team):
        row = table[table["team"] == team]
        return row.iloc[0] if not row.empty else None

    home = team_row(home_team)
    away = team_row(away_team)

    if home is None or away is None:
        return {
            "home_incentive": 0,
            "away_incentive": 0,
            "incentive_diff": 0
        }

    def incentive_score(row):
        pos = int(row["position"])
        if pos <= 4:
            return 3
        elif pos <= 6:
            return 2
        elif pos >= 18:
            return 3
        elif pos >= 15:
            return 2
        else:
            return 1

    home_score = incentive_score(home)
    away_score = incentive_score(away)

    return {
        "home_incentive": home_score,
        "away_incentive": away_score,
        "incentive_diff": home_score - away_score
    }
