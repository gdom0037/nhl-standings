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

# Format as chart
chart = "🏒 NHL Standings\n---------------------\n"
for line in lines:
    line = line.strip()
    if not line:
        continue

    # Preserve headers or notes
    if not line.startswith("{"):
        chart += line + "\n"
        continue

    # Extract dictionary portion
    dict_match = re.match(r"(\{.*?\})", line)
    if not dict_match:
        chart += f"⚠️ Unreadable line: {line}\n"
        continue

    try:
        team_data = ast.literal_eval(dict_match.group(1))
        name = team_data.get("default", "Unknown Team")

        # Extract points from trailing text
        points_match = re.search(r"–\s*(\d+)\s*pts", line)
        points = f"{points_match.group(1)} pts" if points_match else "0 pts"

        chart += f"{name} – {points}\n"
    except Exception:
        chart += f"⚠️ Unreadable line: {line}\n"

chart += "---------------------"

print("✅ Generated chart:")
print(chart)

# Build RSS XML
rss = etree.Element("rss", version="2.0")
channel = etree.SubElement(rss, "channel")
etree.SubElement(channel, "title").text = "GageBot NHL Standings Feed"
etree.SubElement(channel, "link").text = "https://gage.codes/nhl-standings/"
etree.SubElement(channel, "description").text = f"Daily NHL standings updates — {datetime.utcnow().isoformat()}"
etree.SubElement(channel, "language").text = "en-us"
etree.SubElement(channel, "lastBuildDate").text = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

item = etree.SubElement(channel, "item")
etree.SubElement(item, "title").text = chart
etree.SubElement(item, "link").text = "https://gage.codes/nhl-standings/standings.txt"
etree.SubElement(item, "description").text = "Full standings chart embedded in title for dlvr.it"
etree.SubElement(item, "pubDate").text = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

# Write to feed.xml
try:
    with open("feed.xml", "wb") as f:
        f.write(etree.tostring(rss, pretty_print=True, xml_declaration=True, encoding="UTF-8"))
    print("✅ feed.xml successfully written.")
except Exception as e:
    print(f"❌ Failed to write feed.xml: {e}")
