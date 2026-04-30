# viz-336: Closing the Schoolgate - Gender Parity in School Enrollment
# Dataset: wb--SE-ENR-PRSC-FM-ZS (Gender Parity Index for primary+secondary enrollment)
#
# Story: A GPI of 1.0 means equal female-to-male enrollment.
# Below 1.0 means girls are under-enrolled. Many low-income countries
# in 1990 had GPI well below 0.7 - by 2021 most have reached parity,
# while a handful remain stuck.

import json
from pathlib import Path

dataset_path = Path(__file__).resolve().parents[2] / "catalog" / "datasets" / "wb--SE-ENR-PRSC-FM-ZS.json"
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

# For each country: earliest reading >= 1990, latest reading >= 2010
candidates = []
for n, rows in by.items():
    rows = sorted(rows, key=lambda r: r["year"])
    early = next((r for r in rows if r["year"] >= 1990), None)
    late = next((r for r in reversed(rows) if r["year"] >= 2010), None)
    if not early or not late or early["year"] >= late["year"]:
        continue
    if late["year"] - early["year"] < 15:
        continue
    candidates.append({
        "n": n,
        "v0": round(early["value"], 3),
        "y0": early["year"],
        "v1": round(late["value"], 3),
        "y1": late["year"],
        "d": round(late["value"] - early["value"], 3),
    })

# Selection: 12 biggest improvers (started below 0.95) + 4 still struggling
big_movers = sorted([c for c in candidates if c["v0"] < 0.95], key=lambda x: -x["d"])[:12]
still_low = sorted([c for c in candidates if c["v1"] < 0.90 and c not in big_movers],
                    key=lambda x: x["v1"])[:4]

selected = big_movers + still_low
chart_data = sorted(selected, key=lambda r: r["v1"])

if __name__ == "__main__":
    print(json.dumps(chart_data, separators=(",", ":")))
