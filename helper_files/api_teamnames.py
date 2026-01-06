import requests
import os
from collections import defaultdict

API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")
HEADERS = {"X-Auth-Token": API_KEY}

competitions = ["CL"]
seasons = [2023, 2024, 2025]

teams = defaultdict(set)

for comp in competitions:
    for season in seasons:
        url = f"https://api.football-data.org/v4/competitions/{comp}/matches?season={season}"
        r = requests.get(url, headers=HEADERS)
        if r.status_code != 200:
            continue

        for m in r.json().get("matches", []):
            ht = m.get("homeTeam", {}).get("name")
            at = m.get("awayTeam", {}).get("name")
            if ht:
                teams[comp].add(ht)
            if at:
                teams[comp].add(at)

for comp, names in teams.items():
    print(f"\n{comp}")
    for n in sorted(names):
        print(n)
