import requests
import os

API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")

if not API_KEY:
    raise Exception("❌ API key not found")

url = "https://api.football-data.org/v4/competitions/PL/matches"

headers = {
    "X-Auth-Token": API_KEY
}

response = requests.get(url, headers=headers)

print("Status Code:", response.status_code)

if response.status_code == 200:
    data = response.json()
    print("✅ API working")
    print("Competition:", data["competition"]["name"])
    print("Matches returned:", len(data["matches"]))
else:
    print("❌ API error")
    print(response.text)
