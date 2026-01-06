import psycopg2
from db_config_1 import create_connection

# ---------------------------------------
# CANONICAL CURRENT TEAMS (SOURCE OF TRUTH)
# ---------------------------------------

CURRENT_TEAMS = {
    "PL": [
    "Arsenal",
    "Aston Villa",
    "Bournemouth",
    "Brentford",
    "Brighton",
    "Burnley",
    "Chelsea",
    "Crystal Palace",
    "Everton",
    "Fulham",
    "Leeds",
    "Liverpool",
    "Man City",
    "Man United",
    "Newcastle",
    "Nottm Forest",
    "Sunderland",
    "Tottenham",
    "West Ham",
    "Wolves"
    ],
    "PD": [
    "Alaves",
    "Ath Bilbao",
    "Ath Madrid",
    "Barcelona",
    "Celta",
    "Elche",
    "Espanol",
    "Getafe",
    "Girona",
    "Levante",
    "Mallorca",
    "Osasuna",
    "Oviedo",
    "Vallecano",
    "Betis",
    "Real Madrid",
    "Sociedad",
    "Sevilla",
    "Valencia",
    "Villarreal"
    ],
    "SA": [
    "Milan", 
    "Atalanta", 
    "Bologna", 
    "Como", 
    "Cremonese",
    "Fiorentina", 
    "Genoa", 
    "Juventus", 
    "Lecce", 
    "Napoli",
    "Pisa", 
    "Roma", 
    "Sassuolo", 
    "Spezia",
    "Torino", 
    "Udinese", 
    "Verona"
    ],
    "BL1": [
    "Bayern Munich",
    "RB Leipzig",
    "Dortmund",
    "Leverkusen",
    "Hoffenheim",
    "Ein Frankfurt",
    "Stuttgart",
    "Wolfsburg",
    "Werder Bremen",
    "Freiburg",
    "FC Koln",
    "MGladbach",
    "Mainz",
    "Hamburg",
    "Augsburg",
    "Union Berlin",
    "Heidenheim"
    ],
    "FL1": [
    "Angers", 
    "Auxerre", 
    "Brest", 
    "Clermont", 
    "Lorient",
    "Le Havre", 
    "Montpellier", 
    "Paris FC", 
    "Metz",
    "Paris SG", 
    "Monaco",
    "Lyon", 
    "Marseille",
    "Rennes", 
    "Lille", 
    "Nice",
    "Strasbourg", 
    "Toulouse"
    ]
}

# ---------------------------------------
# INSERT LOGIC
# ---------------------------------------

conn = create_connection()
cur = conn.cursor()

inserted = 0

for comp_code, teams in CURRENT_TEAMS.items():
    for team in teams:
        cur.execute("""
            INSERT INTO current_teams_1 (canonical_name, competition_code)
            VALUES (%s, %s)
            ON CONFLICT (canonical_name) DO NOTHING;
        """, (team, comp_code))
        inserted += 1

conn.commit()
cur.close()
conn.close()

print(f"✅ Current teams loaded: {inserted}")
