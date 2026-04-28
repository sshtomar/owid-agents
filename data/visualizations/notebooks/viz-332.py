# viz-332: Tobacco Use Trends - Where Smoking Declined Most (2000 to 2022)
# Dataset: wb--SH-PRV-SMOK (Prevalence of current tobacco use, % of adults)

import json
from pathlib import Path

dataset_path = Path(__file__).resolve().parents[2] / "catalog" / "datasets" / "wb--SH-PRV-SMOK.json"
raw = json.loads(dataset_path.read_text())
data = [r for r in raw["data"] if r["value"] is not None]

# Strip out World Bank regional/income aggregates - keep real countries only
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

by_country = {}
for r in countries:
    by_country.setdefault(r["countryName"], []).append(r)

deltas = []
for n, rows in by_country.items():
    rows.sort(key=lambda r: r["year"])
    if len(rows) < 2:
        continue
    early, late = rows[0], rows[-1]
    if late["year"] - early["year"] < 15:
        continue
    deltas.append({
        "country": n,
        "v0": early["value"],
        "y0": early["year"],
        "v1": late["value"],
        "y1": late["year"],
        "delta": late["value"] - early["value"],
    })

biggest_decline = sorted(deltas, key=lambda x: x["delta"])[:12]
biggest_rise = sorted(deltas, key=lambda x: -x["delta"])[:5]
selected = biggest_decline + biggest_rise

chart_data = [
    {
        "n": r["country"],
        "v0": round(r["v0"], 1),
        "y0": r["y0"],
        "v1": round(r["v1"], 1),
        "y1": r["y1"],
        "d": round(r["delta"], 1),
    }
    for r in selected
]

if __name__ == "__main__":
    print(json.dumps(chart_data, separators=(",", ":")))
