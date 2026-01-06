import requests
import os
import time
from db_config_1 import create_connection

# -------------------------
# CONFIG
# -------------------------
API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")
HEADERS = {"X-Auth-Token": API_KEY}

COMPETITIONS = ["PL", "PD", "SA", "BL1", "FL1", "CL" ]
START_SEASON = 2023
END_SEASON = 2025

# -------------------------
# SOURCE OF TRUTH (KAGGLE NAMES)
# -------------------------
CURRENT_TEAMS = {
    "PL": [
        "Arsenal","Aston Villa","Bournemouth","Brentford","Brighton",
        "Burnley","Chelsea","Crystal Palace","Everton","Fulham","Leeds",
        "Liverpool","Man City","Man United","Newcastle","Nottm Forest",
        "Sunderland","Tottenham","West Ham","Wolves"
    ],
    "PD": [
        "Alaves","Ath Bilbao","Ath Madrid","Barcelona","Celta","Elche",
        "Espanol","Getafe","Girona","Levante","Mallorca","Osasuna",
        "Oviedo","Vallecano","Betis","Real Madrid","Sociedad",
        "Sevilla","Valencia","Villarreal"
    ],
    "SA": [
        "Milan","Atalanta","Bologna","Como","Cremonese","Fiorentina",
        "Genoa","Juventus","Lecce","Napoli","Pisa","Roma",
        "Sassuolo","Spezia","Torino","Udinese","Verona"
    ],
    "BL1": [
        "Bayern Munich","RB Leipzig","Dortmund","Leverkusen","Hoffenheim",
        "Ein Frankfurt","Stuttgart","Wolfsburg","Werder Bremen",
        "Freiburg","FC Koln","MGladbach","Mainz","Hamburg",
        "Augsburg","Union Berlin","Heidenheim"
    ],
    "FL1": [
        "Angers","Auxerre","Brest","Clermont","Lorient","Le Havre",
        "Montpellier","Paris FC","Metz","Paris SG","Monaco","Lyon",
        "Marseille","Rennes","Lille","Nice","Strasbourg","Toulouse"
    ],
    "CL": [
    "Union Berlin",
    "Milan",
    "AC Sparta Praha",
    "AFC Ajax",
    "Monaco",
    "Arsenal",
    "Aston Villa",
    "Atalanta",
    "Ath Bilbao",
    "BSC Young Boys",
    "Leverkusen",
    "Bologna",
    "Dortmund",
    "Celtic FC",
    "Chelsea",
    "Ath Madrid",
    "Club Brugge KV",
    "Ein Frankfurt",
    "Barcelona",
    "Bayern Munich",
    "Inter",
    "FC København",
    "FC Porto",
    "FC Red Bull Salzburg",
    "FK Bodø/Glimt",
    "FK Crvena Zvezda",
    "FK Kairat",
    "FK Shakhtar Donetsk",
    "Feyenoord Rotterdam",
    "GNK Dinamo Zagreb",
    "Galatasaray SK",
    "Girona",
    "Juventus",
    "Lille",
    "Liverpool",
    "Man City",
    "Man United",
    "Newcastle",
    "Marseille",
    "PAE Olympiakos SFP",
    "PSV",
    "Paphos FC",
    "Paris SG",
    "Qarabağ Ağdam FK",
    "RB Leipzig",
    "Lens",
    "Real Madrid",
    "Sociedad",
    "Royal Antwerp FC",
    "Royale Union Saint-Gilloise",
    "SK Slavia Praha",
    "SK Sturm Graz",
    "Lazio",
    "Napoli",
    "Sevilla",
    "Sport Lisboa e Benfica",
    "Sporting Clube de Braga",
    "Sporting Clube de Portugal",
    "Brest",
    "Tottenham",
    "Stuttgart",
    "Villarreal",
    "ŠK Slovan Bratislava"
]
}

# -------------------------
# API → KAGGLE NAME MAP
# -------------------------
TEAM_NAME_MAP = {
    # PL
    "Arsenal FC": "Arsenal",
    "Aston Villa FC": "Aston Villa",
    "AFC Bournemouth": "Bournemouth",
    "Brentford FC": "Brentford",
    "Brighton & Hove Albion FC": "Brighton",
    "Burnley FC": "Burnley",
    "Chelsea FC": "Chelsea",
    "Crystal Palace FC": "Crystal Palace",
    "Everton FC": "Everton",
    "Fulham FC": "Fulham",
    "Leeds United FC": "Leeds",
    "Liverpool FC": "Liverpool",
    "Manchester City FC": "Man City",
    "Manchester United FC": "Man United",
    "Newcastle United FC": "Newcastle",
    "Nottingham Forest FC": "Nottm Forest",
    "Sunderland AFC": "Sunderland",
    "Tottenham Hotspur FC": "Tottenham",
    "West Ham United FC": "West Ham",
    "Wolverhampton Wanderers FC": "Wolves",

    # PD
    "Athletic Club": "Ath Bilbao",
    "Club Atlético de Madrid": "Ath Madrid",
    "Deportivo Alavés": "Alaves",
    "FC Barcelona": "Barcelona",
    "RC Celta de Vigo": "Celta",
    "Elche CF": "Elche",
    "RCD Espanyol de Barcelona": "Espanol",
    "Getafe CF": "Getafe",
    "Girona FC": "Girona",
    "Levante UD": "Levante",
    "RCD Mallorca": "Mallorca",
    "CA Osasuna": "Osasuna",
    "Real Oviedo": "Oviedo",
    "Rayo Vallecano de Madrid": "Vallecano",
    "Real Betis Balompié": "Betis",
    "Real Madrid CF": "Real Madrid",
    "Real Sociedad de Fútbol": "Sociedad",
    "Sevilla FC": "Sevilla",
    "Valencia CF": "Valencia",
    "Villarreal CF": "Villarreal",

    # SA
    "AC Milan": "Milan",
    "Atalanta BC": "Atalanta",
    "Bologna FC 1909": "Bologna",
    "Como 1907": "Como",
    "US Cremonese": "Cremonese",
    "ACF Fiorentina": "Fiorentina",
    "Genoa CFC": "Genoa",
    "Juventus FC": "Juventus",
    "US Lecce": "Lecce",
    "SSC Napoli": "Napoli",
    "AC Pisa 1909": "Pisa",
    "AS Roma": "Roma",
    "US Sassuolo Calcio": "Sassuolo",
    "Torino FC": "Torino",
    "Udinese Calcio": "Udinese",
    "Hellas Verona FC": "Verona",

    # BL1
    "FC Bayern München": "Bayern Munich",
    "RB Leipzig": "RB Leipzig",
    "Borussia Dortmund": "Dortmund",
    "Bayer 04 Leverkusen": "Leverkusen",
    "TSG 1899 Hoffenheim": "Hoffenheim",
    "Eintracht Frankfurt": "Ein Frankfurt",
    "VfB Stuttgart": "Stuttgart",
    "VfL Wolfsburg": "Wolfsburg",
    "SV Werder Bremen": "Werder Bremen",
    "SC Freiburg": "Freiburg",
    "1. FC Köln": "FC Koln",
    "Borussia Mönchengladbach": "MGladbach",
    "1. FSV Mainz 05": "Mainz",
    "FC Augsburg": "Augsburg",
    "1. FC Union Berlin": "Union Berlin",
    "1. FC Heidenheim 1846": "Heidenheim",

    # FL1
    "Angers SCO": "Angers",
    "AJ Auxerre": "Auxerre",
    "Stade Brestois 29": "Brest",
    "Clermont Foot 63": "Clermont",
    "FC Lorient": "Lorient",
    "Le Havre AC": "Le Havre",
    "Montpellier HSC": "Montpellier",
    "Paris FC": "Paris FC",
    "FC Metz": "Metz",
    "Paris Saint-Germain FC": "Paris SG",
    "AS Monaco FC": "Monaco",
    "Olympique Lyonnais": "Lyon",
    "Olympique de Marseille": "Marseille",
    "Stade Rennais FC": "Rennes",
    "LOSC Lille": "Lille",
    "OGC Nice": "Nice",
    "RC Strasbourg Alsace": "Strasbourg",
    "Toulouse FC": "Toulouse",
    # CL - Other European Teams (No matching alias in E0/SP1/I1/D1/F1)
    "AC Sparta Praha": "AC Sparta Praha",
    "AFC Ajax": "AFC Ajax",
    "BSC Young Boys": "BSC Young Boys",
    "Celtic FC": "Celtic FC",
    "Club Brugge KV": "Club Brugge KV",
    "FC København": "FC København",
    "FC Porto": "FC Porto",
    "FC Red Bull Salzburg": "FC Red Bull Salzburg",
    "FK Bodø/Glimt": "FK Bodø/Glimt",
    "FK Crvena Zvezda": "FK Crvena Zvezda",
    "FK Kairat": "FK Kairat",
    "FK Shakhtar Donetsk": "FK Shakhtar Donetsk",
    "Feyenoord Rotterdam": "Feyenoord Rotterdam",
    "GNK Dinamo Zagreb": "GNK Dinamo Zagreb",
    "Galatasaray SK": "Galatasaray SK",
    "PAE Olympiakos SFP": "PAE Olympiakos SFP",
    "PSV": "PSV",
    "Paphos FC": "Paphos FC",
    "Qarabağ Ağdam FK": "Qarabağ Ağdam FK",
    "Royal Antwerp FC": "Royal Antwerp FC",
    "Royale Union Saint-Gilloise": "Royale Union Saint-Gilloise",
    "SK Slavia Praha": "SK Slavia Praha",
    "SK Sturm Graz": "SK Sturm Graz",
    "Sport Lisboa e Benfica": "Sport Lisboa e Benfica",
    "Sporting Clube de Braga": "Sporting Clube de Braga",
    "Sporting Clube de Portugal": "Sporting Clube de Portugal",
    "ŠK Slovan Bratislava": "ŠK Slovan Bratislava"
 }

# -------------------------
# DB
# -------------------------
conn = create_connection()
cur = conn.cursor()

inserted = 0
skipped = 0

# -------------------------
# INGESTION
# -------------------------
for comp in COMPETITIONS:
    kaggle_set = set(CURRENT_TEAMS[comp])

    for season in range(START_SEASON, END_SEASON + 1):
        print(f"Fetching {comp} {season}")

        url = f"https://api.football-data.org/v4/competitions/{comp}/matches?season={season}"
        r = requests.get(url, headers=HEADERS)

        if r.status_code != 200:
            time.sleep(8)
            continue

        for m in r.json().get("matches", []):
            if m.get("status") != "FINISHED":
                continue

            raw_home = m["homeTeam"]["name"]
            raw_away = m["awayTeam"]["name"]

            home = TEAM_NAME_MAP.get(raw_home, raw_home)
            away = TEAM_NAME_MAP.get(raw_away, raw_away)

            # 🔑 ASYMMETRIC RULE
            if home not in kaggle_set and away not in kaggle_set:
                skipped += 1
                continue

            hg = m["score"]["fullTime"]["home"]
            ag = m["score"]["fullTime"]["away"]

            if hg is None or ag is None:
                continue

            result = "H" if hg > ag else "A" if hg < ag else "D"

            cur.execute("""
                INSERT INTO matches_api (
                    match_date, season, competition_code,
                    home_team, away_team,
                    home_goals, away_goals,
                    result, data_source
                )
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,'api')
                ON CONFLICT DO NOTHING
            """, (
                m["utcDate"][:10],
                season,
                comp,
                home,
                away,
                hg,
                ag,
                result
            ))

            inserted += 1

        conn.commit()
        time.sleep(8)

cur.close()
conn.close()

print(f"✅ Inserted: {inserted}")
print(f"⏭️ Skipped: {skipped}")
