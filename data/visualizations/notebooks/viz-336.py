# viz-336: The Happiness Shift - life satisfaction 2011 vs 2025
# Dataset: owid--1210090 (Cantril Ladder, 0-10) from Gallup World Poll / WHR

import json
from pathlib import Path

dataset_path = Path(__file__).resolve().parents[2] / "catalog" / "datasets" / "owid--1210090.json"
raw = json.loads(dataset_path.read_text())
data = [r for r in raw["data"] if r["value"] is not None]

by_country = {}
for r in data:
    by_country.setdefault(r["countryName"], []).append(r)

# Regionally diverse, recognizable mix of major countries -- same selection
# pattern as viz-335 (overweight) so the visual frame is consistent.
selected = [
    "Finland", "Denmark", "Sweden", "Norway", "Iceland",
    "United States", "Canada", "Mexico", "Brazil", "Argentina",
    "United Kingdom", "Germany", "France", "Italy", "Spain",
    "Israel", "Saudi Arabia", "Iran", "Turkey", "Egypt",
    "China", "India", "Japan", "South Korea", "Indonesia",
    "Australia", "South Africa", "Nigeria", "Lebanon", "Afghanistan",
]

points = []
for n in selected:
    rows = sorted(by_country.get(n, []), key=lambda r: r["year"])
    if not rows:
        continue
    early = next((r for r in rows if r["year"] == 2011), None) or rows[0]
    late = next((r for r in rows if r["year"] == 2025), None) or rows[-1]
    if late["year"] == early["year"]:
        continue
    points.append({
        "n": n,
        "v0": round(early["value"], 2),
        "y0": early["year"],
        "v1": round(late["value"], 2),
        "y1": late["year"],
        "d": round(late["value"] - early["value"], 2),
    })

chart_data = sorted(points, key=lambda r: -r["v1"])

if __name__ == "__main__":
    print(json.dumps(chart_data, separators=(",", ":")))
