from db_config_1 import create_connection
from team_normalizer import CURRENT_TEAMS

SEASON = 2024
COMPETITION = "PL"
SOURCE = "fpl"

allowed_teams = CURRENT_TEAMS[COMPETITION]

conn = create_connection()
cur = conn.cursor()

cur.execute("""
    INSERT INTO team_player_features (
        team_name,
        competition_code,
        season,
        avg_form,
        total_minutes,
        attacking_index,
        creativity_index,
        threat_index,
        injury_count,
        source
    )
    SELECT
        team_name,
        competition_code,
        %s,
        AVG(form),
        SUM(minutes),
        AVG(influence),
        AVG(creativity),
        AVG(threat),
        SUM(CASE WHEN status != 'a' THEN 1 ELSE 0 END),
        %s
    FROM player_data
    WHERE competition_code = %s
      AND source = %s
      AND team_name = ANY(%s)
    GROUP BY team_name, competition_code
    ON CONFLICT DO NOTHING;
""", (
    SEASON,
    SOURCE,
    COMPETITION,
    SOURCE,
    allowed_teams
))

conn.commit()
cur.close()
conn.close()

print("✅ Team-level FPL features generated")
