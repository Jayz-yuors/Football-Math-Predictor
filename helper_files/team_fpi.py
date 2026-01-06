import requests

data = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/").json()
teams = [t["name"] for t in data["teams"]]
print(teams)
