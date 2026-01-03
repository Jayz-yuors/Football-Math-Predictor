"""
db_loader.py
============

Purpose
-------
Centralized, SAFE, READ-ONLY access layer for database tables.

Design Philosophy
-----------------
- This file ONLY fetches raw data (no feature logic).
- SQL is used for coarse filtering (league, season, status).
- Pandas handles all downstream logic.
- Functions are added ONLY when reused across multiple modules.

Tables Covered
--------------
- matches_unified
- player_data
- team_player_features
- fixtures_current_season

IMPORTANT
---------
- No writes
- No joins
- No business logic
"""

import pandas as pd
from db_config_1 import create_connection


# ============================================================
# MATCHES (HISTORICAL)
# ============================================================
def load_matches(competition_code: str, season: int):
    """
    Load historical matches for a specific league & season
    """
    query = """
        SELECT *
        FROM matches_unified
        WHERE competition_code = %s
          AND season = %s
          AND status = 'FINISHED'
        ORDER BY match_date
    """

    df = pd.read_sql(
        query,
        conn,
        params=(competition_code, season)
    )

    return df


def load_matches_by_league(competition_code):
    """
    Load all historical matches for a specific league.
    """
    conn = create_connection()
    df = pd.read_sql(
        """
        SELECT *
        FROM matches_unified
        WHERE competition_code = %s
        ORDER BY match_date
        """,
        conn,
        params=(competition_code,)
    )
    conn.close()
    return df
def load_matches_by_league_season(competition_code: str, season: int):
    """
    Load historical matches for a given league & season.
    """
    conn = create_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM matches_unified
        WHERE competition_code = %s
          AND season = %s
        ORDER BY match_date
        """,
        conn,
        params=(competition_code, int(season))
    )

    conn.close()
    return df

# ============================================================
# PLAYER DATA
# ============================================================

def load_player_data():
    """
    Load all player-level data (FPL + Understat).
    """
    conn = create_connection()
    df = pd.read_sql(
        """
        SELECT *
        FROM player_data
        """,
        conn
    )
    conn.close()
    return df

def load_player_data_by_league(competition_code):
    """
    Load current player data for a league (snapshot).
    No season filter by design.
    """
    conn = create_connection()
    df = pd.read_sql(
        """
        SELECT *
        FROM player_data
        WHERE competition_code = %s
        """,
        conn,
        params=(competition_code,)
    )
    conn.close()
    return df



# ============================================================
# TEAM-LEVEL PLAYER FEATURES
# ============================================================

def load_team_player_features():
    """
    Load pre-aggregated team-level player strength metrics.
    """
    conn = create_connection()
    df = pd.read_sql(
        """
        SELECT *
        FROM team_player_features
        """,
        conn
    )
    conn.close()
    return df


def load_team_player_features_by_league(competition_code, season=None):
    """
    Load team player features filtered by league (and optional season).
    """
    conn = create_connection()

    if season:
        df = pd.read_sql(
            """
            SELECT *
            FROM team_player_features
            WHERE competition_code = %s
              AND season = %s
            """,
            conn,
            params=(competition_code, season)
        )
    else:
        df = pd.read_sql(
            """
            SELECT *
            FROM team_player_features
            WHERE competition_code = %s
            """,
            conn,
            params=(competition_code,)
        )

    conn.close()
    return df


# ============================================================
# FIXTURES (CURRENT SEASON)
# ============================================================

def load_fixtures_current_season():
    """
    Load all fixtures of the current season.

    Includes:
    - Past matches (FINISHED)
    - Upcoming matches (SCHEDULED)
    """
    conn = create_connection()
    df = pd.read_sql(
        """
        SELECT *
        FROM fixtures_current_season
        ORDER BY match_date
        """,
        conn
    )
    conn.close()
    return df


def load_fixtures_by_league(competition_code):
    """
    Load fixtures for a specific league.
    """
    conn = create_connection()
    df = pd.read_sql(
        """
        SELECT *
        FROM fixtures_current_season
        WHERE competition_code = %s
        ORDER BY match_date
        """,
        conn,
        params=(competition_code,)
    )
    conn.close()
    return df


def load_upcoming_fixtures(competition_code=None):
    """
    Load only upcoming fixtures (status = SCHEDULED).
    Optional league filter.
    """
    conn = create_connection()

    if competition_code:
        df = pd.read_sql(
            """
            SELECT *
            FROM fixtures_current_season
            WHERE status = 'SCHEDULED'
              AND competition_code = %s
            ORDER BY match_date
            """,
            conn,
            params=(competition_code,)
        )
    else:
        df = pd.read_sql(
            """
            SELECT *
            FROM fixtures_current_season
            WHERE status = 'SCHEDULED'
            ORDER BY match_date
            """,
            conn
        )

    conn.close()
    return df
