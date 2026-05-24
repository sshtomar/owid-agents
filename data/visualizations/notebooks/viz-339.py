# viz-339: Democracy vs Corruption - The Two Faces of Governance (2025)
# Datasets:
#   owid--1209753 (V-Dem Electoral Democracy Index, 0-1)
#   owid--1209730 (V-Dem Political Corruption Index, 0-1)

import json
from pathlib import Path

catalog = Path(__file__).resolve().parents[2] / "catalog" / "datasets"
dem_raw = json.loads((catalog / "owid--1209753.json").read_text())
cor_raw = json.loads((catalog / "owid--1209730.json").read_text())

YEAR = 2025

def latest_by_country(rows):
    out = {}
    for r in rows:
        if r["value"] is None or r["year"] != YEAR:
            continue
        out[r["countryName"]] = r["value"]
    return out

dem = latest_by_country(dem_raw["data"])
cor = latest_by_country(cor_raw["data"])

joined = []
for name in dem:
    if name in cor:
        joined.append({
            "n": name,
            "d": round(dem[name], 3),    # democracy 0-1 (higher = more democratic)
            "c": round(cor[name], 3),    # corruption 0-1 (higher = more corrupt)
        })

# Label only notable / large / interesting countries to avoid clutter
LABEL = {
    "Denmark", "Sweden", "Norway", "Finland", "Switzerland", "Germany",
    "United States", "United Kingdom", "France", "Canada", "Australia",
    "Japan", "South Korea", "Israel", "Estonia",
    "Brazil", "Mexico", "Argentina", "South Africa", "India", "Indonesia",
    "Philippines", "Vietnam", "Pakistan", "Bangladesh", "Nigeria",
    "Hungary", "Turkey", "Russia", "China", "Iran", "Saudi Arabia",
    "Venezuela", "Nicaragua", "El Salvador", "Hong Kong", "Sri Lanka",
    "Singapore", "Egypt", "Ethiopia", "Kenya", "North Korea",
    "Yemen", "Iraq", "Afghanistan",
}

for r in joined:
    r["label"] = r["n"] if r["n"] in LABEL else ""

chart_data = sorted(joined, key=lambda r: -r["d"])

if __name__ == "__main__":
    print(json.dumps(chart_data, separators=(",", ":")))
