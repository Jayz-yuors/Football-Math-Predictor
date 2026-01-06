import os
import requests
from datetime import datetime

from db_config_1 import create_connection
from team_normalizer import normalize_team_name, is_valid_team

# --------------------------------
# CONFIG
# --------------------------------
API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")
HEADERS = {"X-Auth-Token": API_KEY}

SEASON = 2025  # 2025–26
BASE_URL = "https://api.football-data.org/v4/competitions"

LEAGUES = {
    "PL": "PL",
    "PD": "PD",
    "BL1": "BL1",
    "SA": "SA",
    "FL1": "FL1"
}

# --------------------------------
# DB
# --------------------------------
conn = create_connection()
cur = conn.cursor()

inserted = 0
skipped = 0

# --------------------------------
# INGEST
# --------------------------------
for comp, comp_code in LEAGUES.items():
    print(f"📥 Fetching fixtures: {comp_code}")

    url = f"{BASE_URL}/{comp}/matches"
    params = {"season": SEASON}

    r = requests.get(url, headers=HEADERS, params=params, timeout=30)
    r.raise_for_status()

    matches = r.json().get("matches", [])

    for m in matches:
        try:
            match_id = m["id"]
            status = m["status"]

            utc_date = m.get("utcDate")
            match_date = (
                datetime.fromisoformat(utc_date.replace("Z", "")).date()
                if utc_date else None
            )

            matchday = m.get("matchday")

            raw_home = m["homeTeam"]["name"]
            raw_away = m["awayTeam"]["name"]

            home_team = normalize_team_name(raw_home)
            away_team = normalize_team_name(raw_away)

            # Hard league validation
            if not is_valid_team(home_team, comp_code) or not is_valid_team(away_team, comp_code):
                raise ValueError(
                    f"❌ Team not valid for {comp_code}: {home_team} vs {away_team}"
                )

            home_goals = None
            away_goals = None
            result = None

            if status == "FINISHED":
                home_goals = m["score"]["fullTime"]["home"]
                away_goals = m["score"]["fullTime"]["away"]

                if home_goals > away_goals:
                    result = "H"
                elif home_goals < away_goals:
                    result = "A"
                else:
                    result = "D"

            cur.execute("""
                INSERT INTO fixtures_current_season (
                    competition_code,
                    season,
                    match_id,
                    matchday,
                    match_date,
                    home_team,
                    away_team,
                    home_goals,
                    away_goals,
                    result,
                    status
                )
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT (match_id) DO NOTHING;
            """, (
                comp_code,
                SEASON,
                match_id,
                matchday,
                match_date,
                home_team,
                away_team,
                home_goals,
                away_goals,
                result,
                status
            ))

            inserted += 1

        except Exception as e:
            print(e)
            skipped += 1

    conn.commit()

cur.close()
conn.close()

print(f"✅ Fixtures inserted: {inserted}")
print(f"⏭️ Fixtures skipped: {skipped}")
