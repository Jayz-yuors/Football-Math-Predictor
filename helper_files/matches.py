import requests
import os
import time
from db_config_1 import create_connection

# -------------------------
# CONFIG
# -------------------------
API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")
HEADERS = {"X-Auth-Token": API_KEY}

competitions = ["PL", "PD", "SA", "BL1", "FL1", "CL"]
START_SEASON = 2015
END_SEASON = 2025   # free-tier safe window

# -------------------------
# DB CONNECTION
# -------------------------
conn = create_connection()
cur = conn.cursor()

# -------------------------
# HELPER FUNCTION
# -------------------------
def ensure_team_exists(team):
    """
    Inserts team into teams table if valid.
    Safely skips null / placeholder teams.
    """
    if not team:
        return

    team_id = team.get("id")
    if team_id is None:
        return   # very important for CL & future fixtures

    cur.execute("""
        INSERT INTO teams (team_id, name, short_name, tla)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (team_id) DO NOTHING
    """, (
        team_id,
        team.get("name"),
        team.get("shortName"),
        team.get("tla")
    ))

# -------------------------
# MAIN INGESTION LOOP
# -------------------------
for comp in competitions:
    for season in range(START_SEASON, END_SEASON + 1):

        print(f"Fetching {comp} season {season}...")

        url = f"https://api.football-data.org/v4/competitions/{comp}/matches?season={season}"
        response = requests.get(url, headers=HEADERS)

        if response.status_code != 200:
            print(f"⚠️ Skipping {comp} {season} (API error)")
            time.sleep(10)
            continue

        matches = response.json().get("matches", [])

        for m in matches:

            home_team = m.get("homeTeam")
            away_team = m.get("awayTeam")

            # Skip invalid matches (very important)
            if not home_team or not away_team:
                continue
            if home_team.get("id") is None or away_team.get("id") is None:
                continue

            # Ensure teams exist
            ensure_team_exists(home_team)
            ensure_team_exists(away_team)

            # Insert match
            cur.execute("""
                INSERT INTO matches (
                    match_id,
                    competition_code,
                    season,
                    utc_date,
                    matchday,
                    home_team_id,
                    away_team_id,
                    home_goals,
                    away_goals,
                    status
                )
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT (match_id) DO NOTHING
            """, (
                m.get("id"),
                comp,
                season,
                m.get("utcDate"),
                m.get("matchday"),
                home_team.get("id"),
                away_team.get("id"),
                m.get("score", {}).get("fullTime", {}).get("home"),
                m.get("score", {}).get("fullTime", {}).get("away"),
                m.get("status")
            ))

        conn.commit()
        time.sleep(8)  # RATE LIMIT SAFETY

# -------------------------
# CLEANUP
# -------------------------
cur.close()
conn.close()

print("✅ Phase 1.4: API recent matches stored successfully")
