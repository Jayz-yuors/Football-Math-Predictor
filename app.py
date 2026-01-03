"""
run_prediction.py
=================

CLI entry point for live matchday-based prediction
(league-aware, model-aware, table-consistent).
"""

from datetime import date
import pandas as pd
import warnings

# -------------------------------
# SILENCE NON-CRITICAL WARNINGS
# -------------------------------
warnings.filterwarnings(
    "ignore",
    message="pandas only supports SQLAlchemy connectable"
)

from model.utils.db_loader import load_fixtures_current_season
from model.inference.predict_match import predict_match
from model.utils.league_table import fetch_league_table


# -------------------------------
# SUPPORTED LEAGUES
# -------------------------------
LEAGUES = {
    "1": ("PL", "Premier League"),
    "2": ("PD", "La Liga"),
    "3": ("SA", "Serie A"),
    "4": ("BL1", "Bundesliga"),
    "5": ("FL1", "Ligue 1"),
}

SEASON = 2025
MAX_DAY_DIFF = 3   # matchday window (3–4 days)


# -------------------------------
# LEAGUE SELECTION
# -------------------------------
def select_league():
    print("\n🏆 SELECT LEAGUE:\n")
    for k, (_, name) in LEAGUES.items():
        print(f"{k}. {name}")

    while True:
        choice = input("\nEnter choice: ").strip()
        if choice in LEAGUES:
            return LEAGUES[choice]
        print("❌ Invalid league selection.")


# -------------------------------
# FIXTURE HELPERS
# -------------------------------
def get_upcoming_fixtures(league_code: str):
    fixtures = load_fixtures_current_season()

    if fixtures.empty:
        return fixtures

    fixtures = fixtures[
        (fixtures["competition_code"] == league_code) &
        (fixtures["status"].isin(["SCHEDULED", "TIMED"]))
    ].copy()

    today = date.today()

    fixtures["day_diff"] = (
        pd.to_datetime(fixtures["match_date"]).dt.date - today
    ).apply(lambda x: x.days)

    fixtures = fixtures[
        (fixtures["day_diff"] >= 0) &
        (fixtures["day_diff"] <= MAX_DAY_DIFF)
    ]

    return fixtures.sort_values("match_date").reset_index(drop=True)


def select_fixture(fixtures: pd.DataFrame):
    print("\n📅 MATCHDAY FIXTURES:\n")

    for i, row in fixtures.iterrows():
        print(
            f"{i + 1}. {row['home_team']} vs {row['away_team']} "
            f"({row['match_date']})"
        )

    while True:
        try:
            idx = int(input("\nSelect fixture number: ")) - 1
            if 0 <= idx < len(fixtures):
                return fixtures.loc[idx]
        except ValueError:
            pass

        print("❌ Invalid selection. Try again.")


# -------------------------------
# PREDICTION
# -------------------------------
def predict_fixture(fixture: pd.Series) -> dict:
    probs = predict_match(
        competition_code=fixture["competition_code"],
        home_team=fixture["home_team"],
        away_team=fixture["away_team"],
        season=fixture["season"],
        match_date=fixture["match_date"]
    )

    return {
        "home_team": fixture["home_team"],
        "away_team": fixture["away_team"],
        "home_win": probs["home_win"],
        "draw": probs["draw"],
        "away_win": probs["away_win"],
    }


# -------------------------------
# MATCHDAY TABLE SIMULATION
# -------------------------------
def simulate_matchday(fixtures: pd.DataFrame, base_table: pd.DataFrame):

    table = base_table.copy().set_index("team")

    for _, f in fixtures.iterrows():
        probs = predict_fixture(f)

        home = probs["home_team"]
        away = probs["away_team"]

        result = max(
            [("home", probs["home_win"]),
             ("draw", probs["draw"]),
             ("away", probs["away_win"])],
            key=lambda x: x[1]
        )[0]

        table.loc[[home, away], "played"] += 1

        if result == "home":
            table.loc[home, "won"] += 1
            table.loc[home, "points"] += 3
            table.loc[away, "lost"] += 1
            table.loc[home, "goals_for"] += 1
            table.loc[away, "goals_against"] += 1

        elif result == "away":
            table.loc[away, "won"] += 1
            table.loc[away, "points"] += 3
            table.loc[home, "lost"] += 1
            table.loc[away, "goals_for"] += 1
            table.loc[home, "goals_against"] += 1

        else:
            table.loc[[home, away], "drawn"] += 1
            table.loc[[home, away], "points"] += 1
            table.loc[[home, away], "goals_for"] += 1
            table.loc[[home, away], "goals_against"] += 1

    table["goal_difference"] = table["goals_for"] - table["goals_against"]

    table = (
        table.reset_index()
             .sort_values(
                 by=["points", "goal_difference", "goals_for"],
                 ascending=False
             )
             .reset_index(drop=True)
    )

    table["position"] = range(1, len(table) + 1)

    return table


# -------------------------------
# MAIN
# -------------------------------
if __name__ == "__main__":

    league_code, league_name = select_league()

    fixtures = get_upcoming_fixtures(league_code)

    if fixtures.empty:
        print("❌ No upcoming fixtures found.")
        exit()

    selected = select_fixture(fixtures)

    # -------------------------------
    # MATCH PREDICTION
    # -------------------------------
    print("\n🔮 MATCH PREDICTION:\n")
    probs = predict_fixture(selected)

    print(f"{selected['home_team']} WIN % : {probs['home_win']*100:.1f}%")
    print(f"DRAW %            : {probs['draw']*100:.1f}%")
    print(f"{selected['away_team']} WIN % : {probs['away_win']*100:.1f}%")

    # -------------------------------
    # CURRENT TABLE
    # -------------------------------
    current_table = fetch_league_table(
        competition_code=league_code,
        season=SEASON
    )

    print("\n📊 CURRENT LEAGUE TABLE:\n")
    print(current_table.to_string(index=False))

    # -------------------------------
    # SIMULATED TABLE
    # -------------------------------
    print("\n📊 LEAGUE TABLE AFTER MATCHDAY SIMULATION:\n")
    simulated_table = simulate_matchday(fixtures, current_table)
    print(simulated_table.to_string(index=False))
