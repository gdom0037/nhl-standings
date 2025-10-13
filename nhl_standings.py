import requests

url = "https://site.api.espn.com/apis/v2/sports/hockey/nhl/standings"

try:
    response = requests.get(url)
    data = response.json()
    print("✅ ESPN response received.")
except Exception as e:
    print(f"❌ Failed to fetch standings: {e}")
    data = {}

# Debug: Show top-level keys
print("📦 Top-level keys in response:", list(data.keys()))

with open("standings.txt", "w") as f:
    children = data.get("children", [])
    print(f"🔍 Found {len(children)} divisions.")

    for group in children:
        division_name = group.get("name", "Unknown Division")
        format_desc = group.get("standings", {}).get("format", {}).get("description", "")
        f.write(f"{division_name} Standings ({format_desc})\n")

        entries = group.get("standings", {}).get("entries", [])
        print(f"📊 {division_name}: {len(entries)} teams")

        for entry in entries:
            team = entry.get("team", {})
            team_name = team.get("displayName", "Unknown Team")

            stats = {
                stat["name"]: stat["value"]
                for stat in entry.get("stats", [])
                if "name" in stat and "value" in stat
            }

            wins = int(stats.get("wins", 0))
            losses = int(stats.get("losses", 0))
            ot_losses = int(stats.get("otLosses", 0))

            points = wins * 2 + ot_losses
            games_played = wins + losses + ot_losses

            team_dict = {
                "default": team_name,
                "points": points,
                "games_played": games_played
            }

            print(f"✅ Writing team: {team_dict}")
            f.write(str(team_dict) + "\n")

print("✅ standings.txt successfully updated.")
