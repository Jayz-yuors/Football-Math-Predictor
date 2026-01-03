"""
constants.py
-------------
Single source of truth for global constants used across the project.

WHY THIS FILE EXISTS:
- Avoids hardcoding league codes, seasons, paths everywhere
- Prevents mismatch between feature_engineering, training, inference
- Makes future season upgrades trivial

RULES:
- No database access here
- No ML logic here
- Only static configuration & constants
"""

# -------------------------
# SEASONS
# -------------------------
CURRENT_SEASON = 2025          # 2025–26 season
HISTORICAL_START_SEASON = 2000 # For backtests / form windows

# -------------------------
# LEAGUE CODES (Football-Data.org + internal)
# -------------------------
LEAGUES = {
    "PL": "Premier League",
    "PD": "La Liga",
    "BL1": "Bundesliga",
    "SA": "Serie A",
    "FL1": "Ligue 1"
}

# -------------------------
# MATCH RESULT ENCODING
# -------------------------
RESULT_ENCODING = {
    "H": 1,   # Home win
    "D": 0,   # Draw
    "A": -1   # Away win
}

# -------------------------
# POINTS SYSTEM
# -------------------------
POINTS = {
    "WIN": 3,
    "DRAW": 1,
    "LOSS": 0
}

# -------------------------
# DATA EXPORT PATHS
# -------------------------
DATA_EXPORT_PATHS = {
    "matches": "data_export/matches_unified.csv",
    "players": "data_export/player_data.csv",
    "teams": "data_export/team_player_features.csv",
    "fixtures": "data_export/fixtures_current_season.csv"
}

# -------------------------
# MODEL SETTINGS
# -------------------------
TRAIN_TEST_SPLIT_DATE = "2024-07-01"

# -------------------------
# FEATURE ENGINEERING
# -------------------------
FORM_MATCH_WINDOW = 5           # Last N matches
H2H_MATCH_WINDOW = 10            # Last N head-to-head matches
FIXTURE_LOOKAHEAD_MATCHES = 5    # Upcoming matches to consider
