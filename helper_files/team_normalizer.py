# team_normalizer.py

# -------------------------
# SOURCE OF TRUTH
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
        "Sassuolo","Spezia","Torino","Udinese","Verona",
        "Cagliari",
            "Lazio",
            "Inter",
            "Parma",
            "Empoli",
            "Venezia",
            "Monza"
    ],
    "BL1": [
        "Bayern Munich","RB Leipzig","Dortmund","Leverkusen","Hoffenheim",
        "Ein Frankfurt","Stuttgart","Wolfsburg","Werder Bremen",
        "Freiburg","FC Koln","MGladbach","Mainz","Hamburg",
        "Augsburg","Union Berlin","Heidenheim""St. Pauli",
        "Hamburg","Bochum","Darmstadt","Holstein Kiel"
    ],
    "FL1": [
        "Angers","Auxerre","Brest","Clermont","Lorient","Le Havre",
        "Montpellier","Paris FC","Metz","Paris SG","Monaco","Lyon",
        "Marseille","Rennes","Lille","Nice","Strasbourg","Toulouse",
        "Rennes",
        "Lens",
        "Lille",
        "Nantes",
        "Reims",
        "St Etienne"
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
    "Galatasaray SK", ""
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
    "Manchester United": "Man United",
    "Newcastle United FC": "Newcastle",
    "Nottingham Forest": "Nottm Forest",
    "Sunderland AFC": "Sunderland",
    "Tottenham Hotspur": "Tottenham",
    "West Ham United FC": "West Ham",
    "Wolverhampton Wanderers FC": "Wolves",
    "Man Utd": "Man United",
    "Spurs": "Tottenham",
    "Nott'm Forest": "Nottm Forest",
    "Manchester United FC": "Man United",
    "Manchester City FC": "Man City",
    "Tottenham Hotspur FC": "Tottenham",
    "Nottingham Forest FC": "Nottm Forest",
    "Newcastle United FC": "Newcastle",
    "West Ham United FC": "West Ham",
    "Wolverhampton Wanderers FC": "Wolves",
    "Brighton & Hove Albion FC": "Brighton",
    "Crystal Palace FC": "Crystal Palace",
    "Aston Villa FC": "Aston Villa",
    "Arsenal FC": "Arsenal",
    "Leeds United FC": "Leeds",
    "Everton FC": "Everton",
    "Fulham FC": "Fulham",
    "Liverpool FC": "Liverpool",
    "Burnley FC": "Burnley",
    "Chelsea FC": "Chelsea",
    "Brentford FC": "Brentford",
    "AFC Bournemouth": "Bournemouth",

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
    "ŠK Slovan Bratislava": "ŠK Slovan Bratislava",
    #updation required for UNDERSTAT teams
    "Bayer Leverkusen": "Leverkusen",
    "Borussia M.Gladbach": "MGladbach",
    "FC Heidenheim": "Heidenheim",
    "Holstein Kiel": "Holstein Kiel",
    "Mainz 05": "Mainz",
    "RasenBallsport Leipzig": "RB Leipzig",
    "St. Pauli": "St Pauli",

    # SA (Serie A) - Input text variations -> Standard Alias
    "Cagliari": "Cagliari",
    "Empoli": "Empoli",
    "Parma Calcio 1913": "Parma",
    "Venezia": "Venezia",

    # FL1 (Ligue 1) - Input text variations -> Standard Alias
    "Nantes": "Nantes",
    "Paris Saint Germain": "Paris SG",
    "Reims": "Reims",
    "Saint-Etienne": "St Etienne",
    # PD – Understat raw names
"Alaves": "Alaves",
"Atletico Madrid": "Ath Madrid",
"Celta Vigo": "Celta",
"Las Palmas": "Las Palmas",
"Leganes": "Leganes",
"Real Valladolid": "Valladolid",
"Rayo Vallecano": "Vallecano",
# BL1 – Understat raw names
"Bayern Munich": "Bayern Munich",
"Borussia M.Gladbach": "MGladbach",
"RasenBallsport Leipzig": "RB Leipzig",
"Union Berlin": "Union Berlin",
"Holstein Kiel": "Holstein Kiel",
"Bochum": "Bochum",
"St. Pauli": "St. Pauli",
# SA – Understat raw names
"Inter": "Inter",
"Cagliari": "Cagliari",
"Empoli": "Empoli",
"Monza": "Monza",
"Parma Calcio 1913": "Parma",
"Venezia": "Venezia",
"Lazio": "Lazio",
# FL1 – Understat raw names
"Paris Saint Germain": "Paris SG",
"Saint-Etienne": "St Etienne",
"Lens": "Lens",
"Reims": "Reims",
"Nantes": "Nantes",
# Bundesliga – football-data.org raw names
"FC St. Pauli 1910": "St. Pauli",
"Hamburger SV": "Hamburg",
"VfL Bochum 1848": "Bochum",
"SV Darmstadt 98": "Darmstadt",
"Holstein Kiel": "Holstein Kiel",
# Serie A – football-data.org raw names
"Cagliari Calcio": "Cagliari",
"SS Lazio": "Lazio",
"FC Internazionale Milano": "Inter",
"Parma Calcio 1913": "Parma",
"US Cremonese": "Cremonese",
"Empoli FC": "Empoli",
"Venezia FC": "Venezia",
"AC Monza": "Monza",
# Ligue 1 – football-data.org raw names
"Stade Rennais FC 1901": "Rennes",
"Racing Club de Lens": "Lens",
"Lille OSC": "Lille",
"FC Nantes": "Nantes",
"Stade de Reims": "Reims",
"AS Saint-Étienne": "St Etienne",


 }

# -------------------------
# HELPERS
# -------------------------

# team_normalizer.py

"""def normalize_team_name(raw_name, team_map=TEAM_NAME_MAP):
    
    Normalize raw team names from any source (API / FPL / Understat)
    into canonical Kaggle-style names.
    

    if not raw_name:
        return None

    raw_name = raw_name.strip()

    # Direct mapping first
    if raw_name in team_map:
        return team_map[raw_name]

    # Fallback: return as-is (may already be canonical)
    return raw_name

def is_valid_team(team_name, competition_code):
    Hard validation against CURRENT_TEAMS
    return team_name in CURRENT_TEAMS.get(competition_code, [])
"""
# NORMALIZATION
# -------------------------

def normalize_team_name(raw_name, team_map=TEAM_NAME_MAP):
    """
    Normalize raw team names into canonical names.
    HARD FAILS if team is unknown.
    """

    if not raw_name:
        raise ValueError("❌ Empty team name received")

    raw_name = raw_name.strip()

    # 1. Direct mapping
    if raw_name in team_map:
        return team_map[raw_name]

    # 2. Already canonical?
    for teams in CURRENT_TEAMS.values():
        if raw_name in teams:
            return raw_name

    # 3. Hard failure
    raise ValueError(f"❌ Unmapped team name: {raw_name}")


def is_valid_team(team_name, competition_code):
    """Strict validation against CURRENT_TEAMS"""
    return team_name in CURRENT_TEAMS.get(competition_code, [])