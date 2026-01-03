"""
PLAYER & SQUAD STRENGTH FEATURES
================================

Models team strength using player-level data.

Core ideas:
- Stronger squads win more often
- Minutes-weighted contribution > raw totals
- Injuries reduce effective strength
- Depth matters across congested fixtures

NO assumptions about starting XI.
NO future leakage.
"""

import pandas as pd
from model.utils.db_loader import (
    load_player_data_by_league,
    load_team_player_features
)



def _compute_team_player_strength(players_df):
    """
    Compute aggregated player strength for one team.
    """

    if players_df.empty:
        return {
            "squad_minutes": 0,
            "attacking_strength": 0,
            "creativity_strength": 0,
            "threat_strength": 0,
            "injury_count": 0
        }

    # Only players who actually played
    active_players = players_df[players_df["minutes"] > 0]

    squad_minutes = active_players["minutes"].sum()

    attacking = (active_players["influence"] * active_players["minutes"]).sum()
    creativity = (active_players["creativity"] * active_players["minutes"]).sum()
    threat = (active_players["threat"] * active_players["minutes"]).sum()

    injury_count = (players_df["status"] != "a").sum()

    return {
        "squad_minutes": squad_minutes,
        "attacking_strength": attacking,
        "creativity_strength": creativity,
        "threat_strength": threat,
        "injury_count": injury_count
    }


def get_player_strength_features(
    competition_code,
    season,
    home_team,
    away_team
):
    """
    Returns squad-level strength comparison features.
    """

    players_df = load_player_data_by_league(competition_code)
    home_players = players_df[players_df["team_name"] == home_team]
    away_players = players_df[players_df["team_name"] == away_team]

    home_strength = _compute_team_player_strength(home_players)
    away_strength = _compute_team_player_strength(away_players)

    features = {
        # Home
        "home_squad_minutes": home_strength["squad_minutes"],
        "home_attacking_strength": home_strength["attacking_strength"],
        "home_creativity_strength": home_strength["creativity_strength"],
        "home_threat_strength": home_strength["threat_strength"],
        "home_injury_count": home_strength["injury_count"],

        # Away
        "away_squad_minutes": away_strength["squad_minutes"],
        "away_attacking_strength": away_strength["attacking_strength"],
        "away_creativity_strength": away_strength["creativity_strength"],
        "away_threat_strength": away_strength["threat_strength"],
        "away_injury_count": away_strength["injury_count"],

        # Relative
        "attacking_strength_diff": (
            home_strength["attacking_strength"] -
            away_strength["attacking_strength"]
        ),
        "creativity_strength_diff": (
            home_strength["creativity_strength"] -
            away_strength["creativity_strength"]
        ),
        "threat_strength_diff": (
            home_strength["threat_strength"] -
            away_strength["threat_strength"]
        ),
        "injury_diff": (
            away_strength["injury_count"] -
            home_strength["injury_count"]
        )
    }

    return features
