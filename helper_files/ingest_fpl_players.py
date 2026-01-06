import requests
from db_config_1 import create_connection
from team_normalizer import normalize_team_name, CURRENT_TEAMS

# -------------------------
# CONFIG
# -------------------------
FPL_URL = "https://fantasy.premierleague.com/api/bootstrap-static/"
COMPETITION = "PL"
SOURCE = "fpl"

# -------------------------
# FETCH FPL DATA
# -------------------------
response = requests.get(FPL_URL)
response.raise_for_status()
data = response.json()

# FPL team_id → team_name
teams_raw = {t["id"]: t["name"] for t in data["teams"]}

# FPL position mapping
positions = {
    1: "GK",
    2: "DEF",
    3: "MID",
    4: "FWD"
}

# Canonical PL teams (SOURCE OF TRUTH)
allowed_teams = set(CURRENT_TEAMS["PL"])

# -------------------------
# DB
# -------------------------
conn = create_connection()
cur = conn.cursor()

inserted = 0
skipped = 0

# -------------------------
# INGEST PLAYERS
# -------------------------
for p in data["elements"]:
    raw_team = teams_raw.get(p["team"])

    if not raw_team:
        skipped += 1
        continue

    # 🔑 Normalize FPL team name → canonical name
    team = normalize_team_name(raw_team)

    # HARD SAFETY FILTER
    if team not in allowed_teams:
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
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (player_id) DO UPDATE SET
            team_name   = EXCLUDED.team_name,
            minutes     = EXCLUDED.minutes,
            goals       = EXCLUDED.goals,
            assists     = EXCLUDED.assists,
            form        = EXCLUDED.form,
            influence   = EXCLUDED.influence,
            creativity  = EXCLUDED.creativity,
            threat      = EXCLUDED.threat,
            status      = EXCLUDED.status,
            updated_at  = CURRENT_TIMESTAMP;
    """, (
        str(p["id"]),
        p["web_name"],
        team,
        COMPETITION,
        positions[p["element_type"]],
        p["minutes"],
        p["goals_scored"],
        p["assists"],
        float(p["form"]),
        float(p["influence"]),
        float(p["creativity"]),
        float(p["threat"]),
        p["status"],
        SOURCE
    ))

    inserted += 1

conn.commit()
cur.close()
conn.close()

print(f"✅ FPL players inserted: {inserted}")
print(f"⏭️ Players skipped (non-canonical teams): {skipped}")
