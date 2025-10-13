import requests

# ESPN NHL standings endpoint
url = "https://site.api.espn.com/apis/v2/sports/hockey/nhl/standings"

try:
    response = requests.get(url)
    data = response.json()
except Exception as e:
    print(f"❌ Failed to fetch standings: {e}")
    data = {}

with open("standings.txt", "w") as f:
    for group in data.get("children", []):
        division_name = group.get("name", "Unknown Division")
        record_format = group.get("standings", {}).get("format", {}).get("description", "")
        f.write(f"{division_name} Standings ({record_format})\n")

        for team_entry in group.get("standings", {}).get("entries", []):
            team_info = team_entry.get("team", {})
            team_name = team_info.get("displayName", "Unknown Team")

            stats = {
                stat["name"]: stat["value"]
                for stat in team_entry.get("stats", [])
                if "name" in stat and "value" in stat
            }

            wins = int(stats.get("wins", 0))
            losses = int(stats.get("losses", 0))
            ot_losses = int(stats.get("otLosses", 0))

            points = wins * 2 + ot_losses
            games_played = wins + losses + ot_losses

            entry = {
                "default": team_name,
                "points": points,
                "games_played": games_played
            }

            f.write(str(entry) + "\n")

print("✅ standings.txt successfully updated.")
