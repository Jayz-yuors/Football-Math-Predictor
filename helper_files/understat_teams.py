from understat_utils import fetch_understat_players

SEASON = 2024

UNDERSTAT_LEAGUES = {
    "La_liga": "PD",
    "Bundesliga": "BL1",
    "Serie_A": "SA",
    "Ligue_1": "FL1"
}

for us_league, comp_code in UNDERSTAT_LEAGUES.items():
    print(f"\n===== {us_league} ({comp_code}) =====")

    players = fetch_understat_players(us_league, SEASON)

    teams = set()
    for p in players:
        if p.get("team_title"):
            teams.add(p["team_title"])

    for t in sorted(teams):
        print(t)

    print(f"TOTAL TEAMS: {len(teams)}")
