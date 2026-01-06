
from db_config_1 import create_connection
from team_normalizer import normalize_team_name, TEAM_NAME_MAP
from understat_utils import fetch_understat_players

SEASON = 2024
SOURCE = "understat"

UNDERSTAT_LEAGUES = {
    "La_liga": "PD",
    "Bundesliga": "BL1",
    "Serie_A": "SA",
    "Ligue_1": "FL1"
}

conn = create_connection()
cur = conn.cursor()

inserted = 0
skipped = 0

for us_league, comp_code in UNDERSTAT_LEAGUES.items():
    print(f"📥 Fetching {us_league} ({comp_code})")

    players = fetch_understat_players(us_league, SEASON)

    for p in players:
        raw_team = p.get("team_title")
        if not raw_team:
            skipped += 1
            continue

        team = normalize_team_name(raw_team, TEAM_NAME_MAP)

        if not team:
            skipped += 1
            continue

        cur.execute("""
            INSERT INTO player_data (
                player_id,
                player_name,
                team_name,
                competition_code,
                position,
                minutes,
                goals,
                assists,
                form,
                influence,
                creativity,
                threat,
                status,
                source
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'a',%s)
            ON CONFLICT (player_id) DO UPDATE SET
                minutes = EXCLUDED.minutes,
                goals = EXCLUDED.goals,
                assists = EXCLUDED.assists,
                updated_at = CURRENT_TIMESTAMP;
        """, (
            f"u_{p['id']}",
            p["player_name"],
            team,
            comp_code,
            p.get("position", "UNK"),
            int(float(p.get("time", 0))),
            int(float(p.get("goals", 0))),
            int(float(p.get("assists", 0))),
            float(p.get("xG", 0)),
            float(p.get("xG", 0)) * 10,
            float(p.get("xA", 0)) * 10,
            float(p.get("xG", 0)) * 10,
            SOURCE
        ))

        inserted += 1

conn.commit()
cur.close()
conn.close()

print(f"✅ Understat players inserted: {inserted}")
print(f"⏭️ Players skipped: {skipped}")
