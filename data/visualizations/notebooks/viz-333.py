# viz-333: Most Water-Stressed Countries
# Dataset: wb--ER-H2O-FWST-ZS (Freshwater withdrawal as % of available resources)

import json
from pathlib import Path

dataset_path = Path(__file__).resolve().parents[2] / "catalog" / "datasets" / "wb--ER-H2O-FWST-ZS.json"
raw = json.loads(dataset_path.read_text())
data = [r for r in raw["data"] if r["value"] is not None]

AGGREGATES = {
    "World", "OECD members", "European Union", "Euro area",
    "High income", "Low income", "Lower middle income", "Middle income",
    "Upper middle income", "Low & middle income",
    "South Asia", "Sub-Saharan Africa", "East Asia & Pacific",
    "Europe & Central Asia", "Latin America & Caribbean",
    "Middle East & North Africa", "North America", "Arab World",
    "Africa Eastern and Southern", "Africa Western and Central",
    "IDA total", "IBRD only", "IDA & IBRD total",
}

countries = [r for r in data if r["countryName"] not in AGGREGATES]

latest = {}
for r in countries:
    n = r["countryName"]
    if n not in latest or r["year"] > latest[n]["year"]:
        latest[n] = r

top20 = sorted(latest.values(), key=lambda r: -r["value"])[:20]

chart_data = [
    {"n": r["countryName"], "v": round(r["value"], 1), "y": r["year"]}
    for r in top20
]

if __name__ == "__main__":
    print(json.dumps(chart_data, separators=(",", ":")))
