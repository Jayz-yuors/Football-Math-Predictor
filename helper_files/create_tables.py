from db_config_1 import create_connection
conn = create_connection()
cur= conn.cursor()
cur.execute("""
            CREATE TABLE IF NOT EXISTS competitions(
            competition_code VARCHAR(5) PRIMARY KEY,
            name TEXT NOT NULL)""")
cur.execute("""
            CREATE TABLE IF NOT EXISTS teams(
            team_id INTEGER PRIMARY KEY ,
            name TEXT NOT NULL,
            short_name TEXT,
            tla CHAR(3))""")
cur.execute("""
CREATE TABLE IF NOT EXISTS matches (
    match_id INTEGER PRIMARY KEY,
    competition_code VARCHAR(5) NOT NULL,
    season SMALLINT NOT NULL,
    utc_date TIMESTAMP NOT NULL,
    matchday SMALLINT,
    home_team_id INTEGER NOT NULL,
    away_team_id INTEGER NOT NULL,
    home_goals SMALLINT,
    away_goals SMALLINT,
    status VARCHAR(20)
)
""")
conn.commit()
cur.close()
conn.close()

print("✅ Phase 1.1: Tables created successfully (final schema)")