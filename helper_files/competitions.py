from db_config_1 import create_connection
competitions = [
    ("PL","Premier League"),
    ("CL","UEFA Champions League"),
    ("SA","Serie A"),
    ("BL1","Bundesliga"),
    ("PD","La Liga"),
    ("FL1","Ligue 1"),
]
conn = create_connection()
cur = conn.cursor()
for code , name in competitions:
    cur.execute(""" INSERT INTO competitions(competition_code,name)
                VALUES(%s,%s)
                ON CONFLICT (competition_code) DO NOTHING """,(code,name))
conn.commit()
cur.close()
conn.close()

print("✅ Phase 1.2: Competitions stored successfully")
