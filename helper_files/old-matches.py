import requests
import os

BASE_URL = "https://www.football-data.co.uk/mmz4281"
LEAGUES = {
    "E0": "Premier_League",
    "SP1": "La_Liga",
    "I1": "Serie_A",
    "D1": "Bundesliga",
    "F1": "Ligue_1"
}

START_SEASON = 2008
END_SEASON = 2022

SAVE_DIR = "data/csv_historical"
os.makedirs(SAVE_DIR, exist_ok=True)

for season in range(START_SEASON, END_SEASON + 1):
    season_code = f"{str(season)[-2:]}{str(season+1)[-2:]}"  # 0809, 0910, ...

    for league_code, league_name in LEAGUES.items():
        url = f"{BASE_URL}/{season_code}/{league_code}.csv"
        file_name = f"{league_code}_{season_code}.csv"
        file_path = os.path.join(SAVE_DIR, file_name)

        print(f"Downloading {file_name} ...")

        r = requests.get(url)
        if r.status_code == 200:
            with open(file_path, "wb") as f:
                f.write(r.content)
        else:
            print(f"⚠️ Missing: {url}")

print("✅ All historical CSVs downloaded")
