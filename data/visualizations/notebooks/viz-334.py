# viz-334: The Bachelor's Boom - Tertiary Attainment Rises Across Wealthy Nations
# Dataset: wb--SE-TER-CUAT-BA-ZS (Bachelor's or equivalent attainment, % of adults 25+)

import json
from pathlib import Path

dataset_path = Path(__file__).resolve().parents[2] / "catalog" / "datasets" / "wb--SE-TER-CUAT-BA-ZS.json"
raw = json.loads(dataset_path.read_text())
data = [r for r in raw["data"] if r["value"] is not None]

by = {}
for r in data:
    by.setdefault(r["countryName"], []).append(r)

# Countries with clean, long time series
selected_names = ["Canada", "Australia", "Korea, Rep.", "Ireland", "Greece"]

series = {}
for n in selected_names:
    rows = sorted(by.get(n, []), key=lambda r: r["year"])
    rows = [r for r in rows if r["year"] >= 2000]
    series[n] = [{"y": r["year"], "v": round(r["value"], 1)} for r in rows]

chart_data = [{"n": n, "points": pts} for n, pts in series.items()]

if __name__ == "__main__":
    print(json.dumps(chart_data, separators=(",", ":")))
