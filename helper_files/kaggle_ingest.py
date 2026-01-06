import pandas as pd
import psycopg2
from datetime import datetime
from db_config_1 import create_connection

CSV_PATH = "data/kaggle_raw/Matches.csv"
CUTOFF_DATE = datetime(2023, 1, 1)

print("🔹 Loading Kaggle Matches.csv...")
df = pd.read_csv(CSV_PATH, low_memory=False)

# Keep only required columns
REQUIRED_COLS = [
    "MatchDate",
    "HomeTeam",
    "AwayTeam",
    "FTHome",
    "FTAway"
]

df = df[REQUIRED_COLS]

# Convert date
df["MatchDate"] = pd.to_datetime(df["MatchDate"], errors="coerce")

# Drop rows with bad dates or scores
df = df.dropna(subset=["MatchDate", "HomeTeam", "AwayTeam", "FTHome", "FTAway"])

# Filter historical only
df = df[df["MatchDate"] < CUTOFF_DATE]

print(f"🔹 Rows after date + null filtering: {len(df)}")

conn = create_connection()
cur = conn.cursor()

# --------------------------------------------------
# Load alias → team_uid mapping
# --------------------------------------------------
cur.execute("""
    SELECT LOWER(alias_name), team_uid
    FROM team_aliases
""")

alias_map = {row[0]: row[1] for row in cur.fetchall()}

# --------------------------------------------------
# Load current team universe
# --------------------------------------------------
cur.execute("""
    SELECT team_uid
    FROM current_teams
""")

valid_team_uids = {row[0] for row in cur.fetchall()}

# --------------------------------------------------
# INGESTION LOOP
# --------------------------------------------------
inserted = 0
skipped = 0

for _, row in df.iterrows():

    home_name = str(row["HomeTeam"]).strip().lower()
    away_name = str(row["AwayTeam"]).strip().lower()

    home_uid = alias_map.get(home_name)
    away_uid = alias_map.get(away_name)

    # Must resolve BOTH teams
    if not home_uid or not away_uid:
        skipped += 1
        continue

    # Must be current teams
    if home_uid not in valid_team_uids or away_uid not in valid_team_uids:
        skipped += 1
        continue

    try:
        cur.execute("""
            INSERT INTO kaggle_matches_staging (
                match_date,
                home_team_uid,
                away_team_uid,
                home_goals,
                away_goals
            )
            VALUES (%s, %s, %s, %s, %s)
        """, (
            row["MatchDate"].date(),
            home_uid,
            away_uid,
            int(row["FTHome"]),
            int(row["FTAway"])
        ))

        inserted += 1

    except Exception:
        skipped += 1
        conn.rollback()
        continue

conn.commit()
cur.close()
conn.close()

print("✅ Kaggle ingestion completed")
print(f"📥 Inserted rows: {inserted}")
print(f"⏭️ Skipped rows: {skipped}")
