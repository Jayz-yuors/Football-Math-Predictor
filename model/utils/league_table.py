"""
league_table.py
===============

Builds the CURRENT league table dynamically from API match data.
NO DATABASE DEPENDENCY.
"""

import pandas as pd
from team_normalizer import normalize_team_name, TEAM_NAME_MAP
from model.utils.api_client import fetch_matches_api


def fetch_league_table(*, competition_code: str, season: int, as_of_date=None):

    EMPTY_TABLE = pd.DataFrame(columns=[
        "position", "team", "played", "won", "drawn", "lost",
        "points", "goal_difference", "goals_for", "goals_against"
    ])

    matches = fetch_matches_api(
        competition_code=competition_code,
        season=season
    )

    if matches is None or matches.empty:
        return EMPTY_TABLE

    if as_of_date is not None:
        matches = matches[matches["match_date"] < as_of_date]

    table = {}

    for _, row in matches.iterrows():

        if row["status"] != "FINISHED":
            continue

        if row["home_goals"] is None or row["away_goals"] is None:
            continue

        home = normalize_team_name(row["home_team"], TEAM_NAME_MAP)
        away = normalize_team_name(row["away_team"], TEAM_NAME_MAP)

        hg = int(row["home_goals"])
        ag = int(row["away_goals"])

        for t in (home, away):
            table.setdefault(t, {
                "played": 0,
                "won": 0,
                "drawn": 0,
                "lost": 0,
                "points": 0,
                "goals_for": 0,
                "goals_against": 0
            })

        table[home]["played"] += 1
        table[away]["played"] += 1

        table[home]["goals_for"] += hg
        table[home]["goals_against"] += ag
        table[away]["goals_for"] += ag
        table[away]["goals_against"] += hg

        if hg > ag:
            table[home]["won"] += 1
            table[home]["points"] += 3
            table[away]["lost"] += 1
        elif ag > hg:
            table[away]["won"] += 1
            table[away]["points"] += 3
            table[home]["lost"] += 1
        else:
            table[home]["drawn"] += 1
            table[away]["drawn"] += 1
            table[home]["points"] += 1
            table[away]["points"] += 1

    # 🔑 CRITICAL SAFETY
    if not table:
        return EMPTY_TABLE

    df = pd.DataFrame.from_dict(table, orient="index")

    df["goal_difference"] = df["goals_for"] - df["goals_against"]

    df = df.sort_values(
        by=["points", "goal_difference", "goals_for"],
        ascending=False
    )

    df["position"] = range(1, len(df) + 1)

    return (
        df.reset_index()
          .rename(columns={"index": "team"})
          .loc[:, [
              "position", "team", "played", "won", "drawn",
              "lost", "points", "goal_difference",
              "goals_for", "goals_against"
          ]]
    )
