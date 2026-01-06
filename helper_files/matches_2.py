import os
import pandas as pd
import hashlib
import re
from db_config_1 import create_connection

# -------------------------
# CONFIG
# -------------------------
CSV_DIR = "data/csv_historical"

LEAGUE_MAP = {
    "E0": "PL",    # Premier League
    "SP1": "PD",   # La Liga
    "I1": "SA",    # Serie A
    "D1": "BL1",   # Bundesliga
    "F1": "FL1"    # Ligue 1
}

# -------------------------
# HELPERS
# -------------------------
def normalize(name):
    if not isinstance(name, str):
        return None
    name = name.lower().strip()
    name = re.sub(r"[^\w\s]", "", name)
    return name

def generate_match_id(date, home, away, comp):
    base = f"{date}_{home}_{away}_{comp}"
    return int(hashlib.md5(base.encode()).hexdigest()[:8], 16) % 2_000_000_000

# -------------------------
# DB CONNECTION
# -------------------------
conn = create_connection()
cur = conn.cursor()

# Load teams from API-ingested table
cur.execute("SELECT team_id, LOWER(name) FROM teams")
team_map = {name: tid for tid, name in cur.fetchall()}

def get_team_id(name):
    norm = normalize(name)
    if norm is None:
        return None
    return team_map.get(norm)

# -------------------------
# INGESTION
# -------------------------
for file in os.listdir(CSV_DIR):
    if not file.endswith(".csv"):
        continue

    # Skip merged CSVs explicitly
    if file.startswith("merge"):
        continue

    league_code, season_code = file.replace(".csv", "").split("_")

    if league_code not in LEAGUE_MAP:
        continue

    competition_code = LEAGUE_MAP[league_code]
    csv_path = os.path.join(CSV_DIR, file)

    print(f"Ingesting {file}...")

    df = pd.read_csv(csv_path, encoding="latin1")

    required_cols = {"Div", "Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG"}
    if not required_cols.issubset(df.columns):
        print(f"⚠️ Skipping {file} (missing required columns)")
        continue

    for _, row in df.iterrows():

        if pd.isna(row["Date"]) or pd.isna(row["HomeTeam"]) or pd.isna(row["AwayTeam"]):
            continue

        home_id = get_team_id(row["HomeTeam"])
        away_id = get_team_id(row["AwayTeam"])

        if home_id is None or away_id is None:
            continue

        match_id = generate_match_id(
            row["Date"],
            row["HomeTeam"],
            row["AwayTeam"],
            competition_code
        )

        cur.execute("""
            INSERT INTO matches (
                match_id,
                competition_code,
                utc_date,
                home_team_id,
                away_team_id,
                home_goals,
                away_goals,
                status
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,'FINISHED')
            ON CONFLICT (match_id) DO NOTHING
        """, (
            match_id,
            competition_code,
            row["Date"],
            home_id,
            away_id,
            int(row["FTHG"]),
            int(row["FTAG"])
        ))

    conn.commit()

cur.close()
conn.close()

print("✅ Historical CSV ingestion completed successfully")
