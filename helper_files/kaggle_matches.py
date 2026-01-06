import pandas as pd
from db_config_1 import create_connection

CSV_PATH = "data/kaggle_raw/Matches.csv"
CUTOFF_DATE = "2023-01-01"

conn = create_connection()
cur = conn.cursor()

print("Loading Kaggle Matches.csv...")

df = pd.read_csv(
    CSV_PATH,
    low_memory=False
)

# Keep only required columns
df = df[
    [
        "Division",
        "MatchDate",
        "HomeTeam",
        "AwayTeam",
        "FTHome",
        "FTAway",
        "FTResult"
    ]
]

# Convert date
df["MatchDate"] = pd.to_datetime(df["MatchDate"], errors="coerce")

# Drop rows with missing critical data
df = df.dropna(
    subset=["MatchDate", "FTHome", "FTAway", "FTResult"]
)

# Apply cutoff
df = df[df["MatchDate"] < CUTOFF_DATE]

print(f"Filtered rows (valid finished matches): {len(df)}")

# Insert
for _, row in df.iterrows():
    season = row["MatchDate"].year

    cur.execute("""
        INSERT INTO matches_kaggle (
            competition_code,
            season,
            match_date,
            home_team_name,
            away_team_name,
            home_goals,
            away_goals,
            result
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        row["Division"],
        season,
        row["MatchDate"].date(),
        str(row["HomeTeam"]).strip(),
        str(row["AwayTeam"]).strip(),
        int(row["FTHome"]),
        int(row["FTAway"]),
        row["FTResult"]
    ))

conn.commit()
cur.close()
conn.close()

print("✅ Phase 1.7: Kaggle matches ingested successfully")
