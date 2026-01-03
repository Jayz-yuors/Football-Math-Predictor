"""
LEAGUE TABLE FEATURES
=====================

Captures competitive pressure using league table context.

What this models:
- Current league position
- Points gap between teams
- Strategic zones (Title / Top-4 / Mid / Relegation)
- Relative table advantage

Why this matters:
Teams do NOT play all matches equally.
Table position directly affects intensity, risk, and tactics.
"""

from model.utils.league_table import fetch_league_table


def _zone(position: int, total_teams: int) -> str:
    """
    Categorize team into strategic table zones.
    """
    if position <= 1:
        return "TITLE"
    elif position <= 4:
        return "TOP4"
    elif position >= total_teams - 2:
        return "RELEGATION"
    else:
        return "MID"


def get_table_features(
    home_team: str,
    away_team: str,
    competition_code: str,
    season: int,
    match_date
):
    """
    Table-based contextual features:
    - table position difference
    - points difference
    - goal difference difference
    - top-table pressure indicators
    """

    table_df = fetch_league_table(
        competition_code=competition_code,
        season=season,
        as_of_date=match_date
    )

    # -------------------------
    # FAIL-SAFE: EMPTY TABLE
    # -------------------------
    if table_df.empty:
        return {
            "table_pos_diff": 0,
            "points_diff": 0,
            "goal_diff_diff": 0,
            "home_top_pressure": 0,
            "away_top_pressure": 0,
        }

    total_teams = len(table_df)

    home_row = table_df[table_df["team"] == home_team]
    away_row = table_df[table_df["team"] == away_team]

    # -------------------------
    # FAIL-SAFE: TEAM NOT FOUND
    # -------------------------
    if home_row.empty or away_row.empty:
        return {
            "table_pos_diff": 0,
            "points_diff": 0,
            "goal_diff_diff": 0,
            "home_top_pressure": 0,
            "away_top_pressure": 0,
        }

    home = home_row.iloc[0]
    away = away_row.iloc[0]

    return {
        "table_pos_diff": away["position"] - home["position"],
        "points_diff": home["points"] - away["points"],
        "goal_diff_diff": home["goal_difference"] - away["goal_difference"],
        "home_top_pressure": int(home["position"] <= 6),
        "away_top_pressure": int(away["position"] <= 6),
    }
