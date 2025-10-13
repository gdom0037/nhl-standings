from datetime import datetime
from lxml import etree
import ast
import re

# Read standings
try:
    with open("standings.txt", "r") as f:
        lines = f.readlines()
except FileNotFoundError:
    print("❌ standings.txt not found.")
    lines = []

# Parse lines into divisions
divisions = {}
current_division = None

for line in lines:
    line = line.strip()
    if not line:
        continue

    # Detect division header
    if "Division Standings" in line:
        current_division = line
        divisions[current_division] = []
        continue

    # Extract dictionary portion
    dict_match = re.match(r"(\{.*?\})", line)
    if not dict_match or current_division is None:
        continue

    try:
        team_data = ast.literal_eval(dict_match.group(1))
        name = team_data.get("default", "Unknown Team")
        points = int(team_data.get("points", 0))
        games_played = int(team_data.get("games_played", 0))

        max_points = games_played * 3 if games_played else 1
        pct = round(points / max_points, 3) if max_points else 0.0

        divisions[current_division].append(f"{name} – {points} pts ({pct})")
    except Exception:
        divisions[current_division].append(f"⚠️ Unreadable line: {line}")

# Build RSS XML
rss = etree.Element("rss", version="2.0")
channel = etree.SubElement(rss, "channel")
etree.SubElement(channel, "title").text = "GageBot NHL Standings Feed"
etree.SubElement(channel, "link").text = "https://gage.codes/nhl-standings/"
etree.SubElement(channel, "description").text = f"Daily NHL standings updates — {datetime.utcnow().isoformat()}"
etree.SubElement(channel, "language").text = "en-us"
etree.SubElement(channel, "lastBuildDate").text = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

# Add one item per division
for division, teams in divisions.items():
    chart = f"{division}\n---------------------\n"
    chart += "\n".join(teams)
    chart += "\n---------------------"

    item = etree.SubElement(channel, "item")
    etree.SubElement(item, "title").text = chart
    etree.SubElement(item, "link").text = "https://gage.codes/nhl-standings/standings.txt"
    etree.SubElement(item, "description").text = f"{division} standings with points percentage"
    etree.SubElement(item, "pubDate").text = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

# Write to feed.xml
try:
    with open("feed.xml", "wb") as f:
        f.write(etree.tostring(rss, pretty_print=True, xml_declaration=True, encoding="UTF-8"))
    print("✅ feed.xml successfully written.")
except Exception as e:
    print(f"❌ Failed to write feed.xml: {e}")
