# viz-336: The World's Happiest Countries in 2025
# Dataset: owid--1210090 (Cantril Ladder, 0-10) from Gallup World Poll / WHR

import json
from pathlib import Path

dataset_path = Path(__file__).resolve().parents[2] / "catalog" / "datasets" / "owid--1210090.json"
raw = json.loads(dataset_path.read_text())
data = [r for r in raw["data"] if r["value"] is not None]

# Latest year only
latest_year = max(r["year"] for r in data)
latest = [r for r in data if r["year"] == latest_year]
latest.sort(key=lambda r: -r["value"])

# Pull rank-anchored slices: top 15, plus a middle and bottom selection so
# the chart spans the full distribution without 160 bars.
top = latest[:15]

# Middle: ranks 30, 50, 75, 100
n = len(latest)
mid_ranks = [29, 49, 74, 99]
middle = [latest[i] for i in mid_ranks if i < n]

# Bottom 10
bottom = latest[-10:]

# Earliest year for each selected country - to show change since 2011
by_country = {}
for r in data:
    by_country.setdefault(r["countryName"], []).append(r)

selected = top + middle + bottom
chart_data = []
for rank, r in enumerate(selected, start=1):
    name = r["countryName"]
    rows = sorted(by_country[name], key=lambda x: x["year"])
    earliest = rows[0]
    chart_data.append({
        "n": name,
        "v": round(r["value"], 2),
        "y": r["year"],
        "v0": round(earliest["value"], 2),
        "y0": earliest["year"],
        "rank": latest.index(r) + 1,
        "group": "top" if r in top else ("mid" if r in middle else "bottom"),
    })

if __name__ == "__main__":
    print(json.dumps(chart_data, separators=(",", ":")))
