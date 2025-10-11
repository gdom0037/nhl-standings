from datetime import datetime
from lxml import etree

# Read standings
with open("standings.txt", "r") as f:
    lines = f.readlines()

# Format as chart
chart = "🏒 NHL Standings\n---------------------\n"
for line in lines:
    chart += line.strip() + "\n"
chart += "---------------------"

# Build RSS XML
rss = etree.Element("rss", version="2.0")
channel = etree.SubElement(rss, "channel")
etree.SubElement(channel, "title").text = "GageBot NHL Standings Feed"
etree.SubElement(channel, "link").text = "https://gdom0037.github.io/nhl-standings/"
etree.SubElement(channel, "description").text = "Daily NHL standings updates from GageBot"
etree.SubElement(channel, "language").text = "en-us"
etree.SubElement(channel, "lastBuildDate").text = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

item = etree.SubElement(channel, "item")
etree.SubElement(item, "title").text = chart
etree.SubElement(item, "link").text = "https://gdom0037.github.io/nhl-standings/standings.txt"
etree.SubElement(item, "pubDate").text = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

# Write to feed.xml
with open("feed.xml", "wb") as f:
    f.write(etree.tostring(rss, pretty_print=True, xml_declaration=True, encoding="UTF-8"))
