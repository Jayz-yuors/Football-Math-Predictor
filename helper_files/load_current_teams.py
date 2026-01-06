from db_config_1 import create_connection

FILE_PATH = "data/current_teams_names.txt"

SECTION_MAP = {
    "1": "PL",
    "2": "PD",
    "3": "SA",
    "4": "BL1",
    "5": "CL",
    "6": "FL1"
}

conn = create_connection()
cur = conn.cursor()

current_competition = None

with open(FILE_PATH, "r", encoding="utf-8") as f:
    for raw_line in f:
        line = raw_line.strip()

        if not line:
            continue

        # Section headers: "1) Premier League"
        if line[0].isdigit() and ")" in line:
            section_num = line.split(")")[0]
            current_competition = SECTION_MAP.get(section_num)

            if not current_competition:
                raise ValueError(f"Unknown section header: {line}")

            continue

        team_name = line

        # Insert team
        cur.execute("""
            INSERT INTO teams_master (canonical_name)
            VALUES (%s)
            ON CONFLICT (canonical_name) DO NOTHING
            RETURNING team_uid
        """, (team_name,))

        row = cur.fetchone()
        if row:
            team_uid = row[0]
        else:
            cur.execute(
                "SELECT team_uid FROM teams_master WHERE canonical_name = %s",
                (team_name,)
            )
            team_uid = cur.fetchone()[0]

        # Insert team → competition mapping
        cur.execute("""
            INSERT INTO team_competitions (team_uid, competition_code)
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING
        """, (team_uid, current_competition))

conn.commit()
cur.close()
conn.close()

print("✅ Current teams loaded into teams_master and team_competitions")
