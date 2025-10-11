from datetime import datetime
from lxml import etree
import ast

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
    if not line.startswith("{"):
        chart += line + "\n"  # Preserve headers or notes
        continue
    try:
        team_data = ast.literal_eval(line)
        name = team_data.get("default", "Unknown Team")
        points = team_data.get("points", "0 pts")
        chart += f"{name} – {points}\n"
    except Exception as e:
        chart += f"⚠️ Error parsing line: {line}\n"
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
etree.SubElement(item, "title").text = chart  # ✅ Embed full chart here for dlvr.it
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
