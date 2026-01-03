"""
api_client.py
=============

Fetches match data from football-data API.
Used ONLY for live league table & fixture logic.
"""

import os
import requests
import pandas as pd
from datetime import datetime

BASE_URL = "https://api.football-data.org/v4"

# --------------------------------
# ENV TOKEN (MANDATORY)
# --------------------------------
API_TOKEN = os.getenv("FOOTBALL_DATA_API_KEY")

if not API_TOKEN:
    raise RuntimeError(
        "❌ FOOTBALL_DATA_API_KEY not set in environment variables"
    )

HEADERS = {
    "X-Auth-Token": API_TOKEN
}

# --------------------------------
# SIMPLE IN-MEMORY CACHE
# --------------------------------
_MATCH_CACHE = {}


def fetch_matches_api(*, competition_code: str, season: int) -> pd.DataFrame:
    """
    Fetch all matches for a league season from API.
    Cached per (competition, season).
    """

    cache_key = (competition_code, season)
    if cache_key in _MATCH_CACHE:
        return _MATCH_CACHE[cache_key]

    url = f"{BASE_URL}/competitions/{competition_code}/matches?season={season}"

    try:
        response = requests.get(url, headers=HEADERS, timeout=20)
    except requests.RequestException as e:
        print(f"❌ API request failed: {e}")
        return pd.DataFrame()

    if response.status_code != 200:
        print(f"❌ API error {response.status_code}: {response.text[:200]}")
        return pd.DataFrame()

    matches = response.json().get("matches", [])
    rows = []

    for m in matches:
        try:
            rows.append({
                "match_date": datetime.fromisoformat(
                    m["utcDate"].replace("Z", "")
                ).date(),
                "home_team": m["homeTeam"]["name"],
                "away_team": m["awayTeam"]["name"],
                "home_goals": m["score"]["fullTime"]["home"],
                "away_goals": m["score"]["fullTime"]["away"],
                "status": m["status"],
            })
        except Exception:
            # Skip malformed API rows safely
            continue

    df = pd.DataFrame(rows)
    _MATCH_CACHE[cache_key] = df
    return df
