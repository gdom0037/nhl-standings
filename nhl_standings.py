import requests
import pandas as pd

url = "https://api-web.nhle.com/v1/standings/now"
response = requests.get(url)
data = response.json()

teams = []
for record in data['standings']:
    RW = record['regulationWins']
    total_wins = record['wins']
    OTW = total_wins - RW
    OTL = record['otLosses']
    RL = record['losses'] - OTL

    teams.append({
        'Team': record['teamName'],
        'Division': record['divisionName'],
        'Conference': record['conferenceName'],
        'GP': record['gamesPlayed'],
        'RW': RW,
        'OTW': OTW,
        'OTL': OTL,
        'RL': RL,
    })

df = pd.DataFrame(teams)
df['Points'] = df['RW'] * 3 + df['OTW'] * 2 + df['OTL']
df['Points %'] = (df['Points'] / (df['GP'] * 3)).round(3)

def format_group(title, group_df):
    group_df = group_df.sort_values(by='Points', ascending=False)
    lines = [f"🏒 {title} Standings (3-2-1-0)"]
    for _, row in group_df.iterrows():
        lines.append(f"{row['Team']} – {row['Points']} pts ({row['Points %']})")
    return "\n".join(lines)

output = []

for division in df['Division'].unique():
    output.append(format_group(f"{division} Division", df[df['Division'] == division]))

for conference in df['Conference'].unique():
    output.append(format_group(f"{conference} Conference", df[df['Conference'] == conference]))

output.append(format_group("League", df))

with open("standings.txt", "w", encoding="utf-8") as f:
    for section in output:
        f.write(section + "\n\n")
