import re
import unicodedata
from db_config_1 import create_connection

# -------------------------------------------------
# 1. Kaggle aliases per canonical team (EXPLICIT)
# -------------------------------------------------
KAGGLE_ALIAS_MAP = {

    # --- PREMIER LEAGUE ---
    "arsenal": ["arsenal fc"],
    "aston villa": ["aston villa fc"],
    "bournemouth": ["afc bournemouth"],
    "brentford": ["brentford fc"],
    "brighton & hove albion": [
        "brighton",
        "brighton and hove albion"
    ],
    "burnley": ["burnley fc"],
    "chelsea": ["chelsea fc"],
    "crystal palace": ["crystal palace fc"],
    "everton": ["everton fc"],
    "fulham": ["fulham fc"],
    "leeds united": ["leeds"],
    "liverpool": ["liverpool fc"],
    "manchester city": [
        "man city",
        "manchester city fc"
    ],
    "manchester united": [
        "man united",
        "man utd",
        "manchester united fc"
    ],
    "newcastle united": [
        "newcastle",
        "newcastle utd"
    ],
    "nottingham forest": [
        "nottingham forest fc"
    ],
    "sunderland": ["sunderland afc"],
    "tottenham hotspur": ["tottenham", "spurs"],
    "west ham united": ["west ham", "west ham utd"],
    "wolverhampton wanderers": ["wolves", "wolverhampton"],

    # --- LA LIGA ---
    "alavés": ["alaves", "deportivo alaves"],
    "athletic bilbao": ["athletic club"],
    "atlético madrid": [
        "ath madrid",
        "atletico madrid"
    ],
    "barcelona": ["barca", "fc barcelona"],
    "celta vigo": ["celta", "rc celta"],
    "elche": ["elche cf"],
    "espanyol": ["rcd espanyol"],
    "getafe": ["getafe cf"],
    "girona": ["girona fc"],
    "levante": ["levante ud"],
    "mallorca": ["rcd mallorca"],
    "osasuna": ["ca osasuna"],
    "oviedo": ["real oviedo"],
    "rayo vallecano": ["rayo vallecano"],
    "real betis": ["real betis balompie"],
    "real madrid": ["real madrid cf"],
    "real sociedad": ["real sociedad"],
    "sevilla": ["sevilla fc"],
    "valencia": ["valencia cf"],
    "villarreal": ["villarreal cf"],

    # --- SERIE A ---
    "ac milan": ["ac milan"],
    "atalanta": ["atalanta bc"],
    "bologna": ["bologna fc"],
    "como": ["como 1907"],
    "cremonese": ["us cremonese"],
    "fiorentina": ["acf fiorentina"],
    "genoa": ["genoa cfc"],
    "inter milan": [
        "inter milan",
        "internazionale"
    ],
    "juventus": ["juventus fc", "juve"],
    "lecce": ["us lecce"],
    "napoli": ["ssc napoli"],
    "pisa": ["pisa sc"],
    "roma": ["as roma"],
    "sassuolo": ["us sassuolo"],
    "spezia": ["spezia calcio"],
    "torino": ["torino fc"],
    "udinese": ["udinese calcio"],
    "verona": ["hellas verona"],

    # --- BUNDESLIGA ---
    "bayern munich": [
        "bayern",
        "fc bayern",
        "fc bayern munchen"
    ],
    "rb leipzig": ["rb leipzig", "rbl"],
    "borussia dortmund": ["dortmund", "bvb"],
    "bayer 04 leverkusen": [
        "leverkusen",
        "bayer leverkusen"
    ],
    "tsg hoffenheim": ["hoffenheim"],
    "eintracht frankfurt": ["frankfurt", "sge"],
    "vfb stuttgart": ["stuttgart"],
    "vfl wolfsburg": ["wolfsburg"],
    "sv werder bremen": ["werder bremen", "werder"],
    "sc freiburg": ["freiburg"],
    "fc köln": ["koln", "fc koln"],
    "borussia mönchengladbach": ["gladbach"],
    "fsv mainz 05": ["mainz", "mainz 05"],
    "hamburger sv": ["hamburg", "hsv"],
    "fc augsburg": ["augsburg"],
    "fc union berlin": ["union berlin"],
    "heidenheim": ["fc heidenheim"],

    # --- UEFA / EUROPE ---
    "ajax": ["afc ajax"],
    "benfica": ["sl benfica"],
    "psv eindhoven": ["psv"],
    "sporting cp": ["sporting", "sporting lisbon"],
    "olympiacos": ["olympiacos fc"],
    "as monaco": ["as monaco"],
    "galatasaray": ["galatasaray sk"],
    "union saint-gilloise (union sg)": ["union sg","rusg","union saint gilloise"],
    "qarabağ": ["qarabag", "qarabag fk"],
    "club brugge": ["club brugge kv"],
    "slavia praha": ["slavia prague"],
    "copenhagen": ["fc copenhagen"],
    "pafos fc": ["pafos"],
    "bodø/glimt": ["bodo glimt"],

    # --- LIGUE 1 ---
    "angers": ["angers sco"],
    "auxerre": ["aj auxerre"],
    "brest": ["stade brestois"],
    "clermont": ["clermont foot"],
    "fc lorient": ["lorient"],
    "le havre": ["le havre ac"],
    "montpellier": ["montpellier hsc"],
    "paris fc": ["paris fc"],
    "metz": ["fc metz"],
    "paris saint-germain (psg)": ["psg","paris saint germain"],
    "olympique lyonnais": ["olympique lyonnais", "lyon"],
    "olympique de marseille": ["olympique de marseille", "marseille"],
    "stade rennais": ["rennes"],
    "losc lille": ["lille", "losc"],
    "ogc nice": ["nice"],
    "rc strasbourg alsace": ["strasbourg"],
    "toulouse fc": ["toulouse"]
}


# -------------------------------------------------
# 2. Normalization helper (DB-safe)
# -------------------------------------------------
def normalize(name: str) -> str:
    name = name.lower().strip()
    name = unicodedata.normalize("NFKD", name)
    name = "".join(c for c in name if not unicodedata.combining(c))
    name = re.sub(r"[^\w\s]", "", name)
    name = re.sub(r"\s+", " ", name)
    return name.strip()

# -------------------------------------------------
# 3. Load canonical teams from DB
# -------------------------------------------------
conn = create_connection()
cur = conn.cursor()

cur.execute("""
    SELECT team_uid, canonical_name
    FROM teams_master
""")

canonical_uid_map = {
    normalize(name): uid
    for uid, name in cur.fetchall()
}

# -------------------------------------------------
# 4. Insert aliases
# -------------------------------------------------
inserted = 0
skipped = 0

for canonical_name, aliases in KAGGLE_ALIAS_MAP.items():
    norm_canonical = normalize(canonical_name)

    if norm_canonical not in canonical_uid_map:
        print(f"⚠️ Canonical team not found in DB: {canonical_name}")
        skipped += len(aliases)
        continue

    team_uid = canonical_uid_map[norm_canonical]

    for alias in aliases:
        cur.execute("""
            INSERT INTO team_aliases (alias_name, team_uid, source)
            VALUES (%s, %s, 'kaggle')
            ON CONFLICT DO NOTHING
        """, (alias, team_uid))

        inserted += 1

conn.commit()
cur.close()
conn.close()

print("✅ Kaggle aliases inserted via dictionaries")
print(f"📌 Aliases inserted: {inserted}")
print(f"⏭️ Skipped (missing canonical): {skipped}")
