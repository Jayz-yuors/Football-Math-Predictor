import requests
import os
import time
from db_config_1 import create_connection

API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")
HEADERS = {"X-Auth-Token": API_KEY}

competitions = ["PL", "PD", "SA", "BL1", "FL1"]

conn = create_connection()
cur = conn.cursor()

for comp in competitions:
    print(f"Fetching teams for {comp}...")
    url = f"https://api.football-data.org/v4/competitions/{comp}/teams"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print(f"⚠️ Failed to fetch teams for {comp}")
        time.sleep(10)
        continue

    teams = response.json().get("teams", [])

    for team in teams:
        cur.execute("""
            INSERT INTO teams (team_id, name, short_name, tla)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (team_id) DO NOTHING
        """, (
            team["id"],
            team["name"],
            team.get("shortName"),
            team.get("tla")
        ))

    conn.commit()
    time.sleep(8)   # Respect rate limits

cur.close()
conn.close()

print("✅ Phase 1.3: Teams stored successfully")
