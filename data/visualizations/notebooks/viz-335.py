# viz-335: The Global Weight Gain - Overweight Prevalence 1990 vs 2022
# Dataset: wb--SH-STA-OWAD-ZS (Prevalence of overweight, % of adults)

import json
from pathlib import Path

dataset_path = Path(__file__).resolve().parents[2] / "catalog" / "datasets" / "wb--SH-STA-OWAD-ZS.json"
raw = json.loads(dataset_path.read_text())
data = [r for r in raw["data"] if r["value"] is not None]

AGGREGATES = {
    "World", "OECD members", "European Union", "Euro area",
    "High income", "Low income", "Lower middle income", "Middle income",
    "Upper middle income", "Low & middle income",
    "South Asia", "South Asia (IDA & IBRD)", "Sub-Saharan Africa",
    "Sub-Saharan Africa (IDA & IBRD countries)",
    "Sub-Saharan Africa (excluding high income)",
    "East Asia & Pacific", "East Asia & Pacific (IDA & IBRD countries)",
    "East Asia & Pacific (excluding high income)",
    "Europe & Central Asia", "Europe & Central Asia (IDA & IBRD countries)",
    "Europe & Central Asia (excluding high income)",
    "Latin America & Caribbean",
    "Latin America & Caribbean (excluding high income)",
    "Latin America & the Caribbean (IDA & IBRD countries)",
    "Middle East & North Africa", "Middle East & North Africa (IDA & IBRD countries)",
    "Middle East & North Africa (excluding high income)",
    "North America", "Arab World", "Pacific island small states",
    "Caribbean small states", "Other small states", "Small states",
    "Heavily indebted poor countries (HIPC)", "Least developed countries: UN classification",
    "Pre-demographic dividend", "Post-demographic dividend",
    "Early-demographic dividend", "Late-demographic dividend",
    "IBRD only", "IDA & IBRD total", "IDA blend", "IDA only", "IDA total",
    "Africa Eastern and Southern", "Africa Western and Central",
    "Fragile and conflict affected situations",
}
countries = [r for r in data if r["countryName"] not in AGGREGATES]

by = {}
for r in countries:
    by.setdefault(r["countryName"], []).append(r)

# Pick a regionally-diverse, recognizable mix
selected = ["United States", "Mexico", "Chile", "Brazil", "Argentina",
            "United Kingdom", "Germany", "France", "Italy", "Spain",
            "China", "India", "Japan", "Korea, Rep.", "Indonesia",
            "South Africa", "Nigeria", "Ethiopia", "Egypt, Arab Rep.",
            "Saudi Arabia", "Iran, Islamic Rep.", "Australia"]

points = []
for n in selected:
    rows = sorted(by.get(n, []), key=lambda r: r["year"])
    if not rows:
        continue
    early = next((r for r in rows if r["year"] == 1990), None) or rows[0]
    late = next((r for r in rows if r["year"] == 2022), None) or rows[-1]
    if late["year"] - early["year"] < 20:
        continue
    points.append({
        "n": n,
        "v0": round(early["value"], 1),
        "y0": early["year"],
        "v1": round(late["value"], 1),
        "y1": late["year"],
        "d": round(late["value"] - early["value"], 1),
    })

chart_data = sorted(points, key=lambda r: -r["v1"])

if __name__ == "__main__":
    print(json.dumps(chart_data, separators=(",", ":")))
