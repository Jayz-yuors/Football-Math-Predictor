from db_config_1 import create_connection

SEASON = 2024
SOURCE = "understat"

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
        NULL,
        SUM(minutes),
        AVG(influence),
        AVG(creativity),
        AVG(threat),
        0,
        %s
    FROM player_data
    WHERE source = %s
    GROUP BY team_name, competition_code
    ON CONFLICT DO NOTHING;
""", (SEASON, SOURCE, SOURCE))

conn.commit()
cur.close()
conn.close()

print("✅ Understat team-level features generated")
