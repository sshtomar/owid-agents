# viz-336: The Happiness Shift 2011-2025
# Dataset: owid--1210090 (Cantril Ladder, 0-10)
# Style: time-series lines for a curated selection of countries, full 2011-2025 range.

import json
from pathlib import Path

dataset_path = Path(__file__).resolve().parents[2] / "catalog" / "datasets" / "owid--1210090.json"
raw = json.loads(dataset_path.read_text())
data = [r for r in raw["data"] if r["value"] is not None]

# Curated 10-country selection: top happiness anchor, biggest movers, major economies.
# Keeping the count near 10 keeps each line readable (Cleveland: limit categories).
selected = [
    "Finland",            # always #1
    "United States",      # major economy in decline
    "Germany",            # rising
    "China",              # biggest gainer
    "India",              # large country decline
    "Canada",             # sharp decline
    "Mexico",             # surprising performer
    "Lebanon",            # crisis-driven collapse
    "Egypt",              # major decline
    "Afghanistan",        # most extreme collapse
]

filtered = [r for r in data if r["countryName"] in selected]
chart_data = sorted(
    [{"n": r["countryName"], "y": r["year"], "v": round(r["value"], 2)} for r in filtered],
    key=lambda r: (r["n"], r["y"]),
)

if __name__ == "__main__":
    print(json.dumps(chart_data, separators=(",", ":")))
