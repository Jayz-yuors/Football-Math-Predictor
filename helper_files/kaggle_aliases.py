import pandas as pd
import unicodedata
import re
from db_config_1 import create_connection

CSV_PATH = "data/kaggle_raw/Matches.csv"

def normalize(name: str) -> str:
    name = name.lower().strip()

    # Remove accents (Atlético → atletico)
    name = unicodedata.normalize("NFKD", name)
    name = "".join(c for c in name if not unicodedata.combining(c))

    # Remove punctuation
    name = re.sub(r"[^\w\s]", "", name)

    # Remove common suffixes
    for token in [" fc", " cf", " afc"]:
        if name.endswith(token):
            name = name.replace(token, "")

    # Collapse spaces
    name = re.sub(r"\s+", " ", name)

    return name.strip()

print("🔹 Loading Kaggle team names...")
df = pd.read_csv(
    CSV_PATH,
    usecols=["HomeTeam", "AwayTeam"],
    low_memory=False
)

kaggle_names = set(df["HomeTeam"].dropna().unique()) | set(df["AwayTeam"].dropna().unique())

conn = create_connection()
cur = conn.cursor()

# Load canonical teams
cur.execute("""
    SELECT team_uid, canonical_name
    FROM teams_master
""")

canonical_map = {
    normalize(name): uid
    for uid, name in cur.fetchall()
}

inserted = 0
skipped = 0

for raw_name in kaggle_names:
    norm = normalize(raw_name)

    if norm in canonical_map:
        team_uid = canonical_map[norm]

        cur.execute("""
            INSERT INTO team_aliases (alias_name, team_uid, source)
            VALUES (%s, %s, 'kaggle')
            ON CONFLICT DO NOTHING
        """, (norm, team_uid))

        inserted += 1
    else:
        skipped += 1

conn.commit()
cur.close()
conn.close()

print("✅ Kaggle alias generation complete")
print(f"📌 Aliases inserted: {inserted}")
print(f"⏭️ Unmatched Kaggle names: {skipped}")
