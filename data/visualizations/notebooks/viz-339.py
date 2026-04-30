# viz-339: Guns versus GDP - Military Spending in 2024
# Dataset: wb--MS-MIL-XPND-GD-ZS (Military expenditure, % of GDP)
#
# Story: Israel and Algeria spend the largest shares of GDP on the
# military, while a cluster of post-Soviet states and frontline
# NATO members (Estonia, Greece) have pushed spending well above
# the alliance's 2% target. The list is dominated by countries near
# active or potential conflicts.

import json
from pathlib import Path

dataset_path = Path(__file__).resolve().parents[2] / "catalog" / "datasets" / "wb--MS-MIL-XPND-GD-ZS.json"
raw = json.loads(dataset_path.read_text())
data = [r for r in raw["data"] if r["value"] is not None]

# WB aggregate country codes (regions/income groups)
AGGREGATE_CODES = {
    "1A", "1W", "4E", "7E", "8S", "B8", "EU", "F1", "OE",
    "S1", "S2", "S3", "S4", "T2", "T3", "T4", "T5", "T6", "T7",
    "V1", "V2", "V3", "V4", "XC", "XD", "XE", "XF", "XG",
    "XH", "XI", "XJ", "XL", "XM", "XN", "XO", "XP", "XQ",
    "XT", "XU", "Z4", "Z7", "ZF", "ZG", "ZH", "ZI", "ZJ", "ZQ", "ZT",
}
data = [r for r in data if r["country"] not in AGGREGATE_CODES]

# Latest reading per country
latest = {}
for r in data:
    cur = latest.get(r["countryName"])
    if cur is None or r["year"] > cur["year"]:
        latest[r["countryName"]] = r

# Use only the most recent year (2024) so the comparison is apples-to-apples
recent = [r for r in latest.values() if r["year"] == 2024]

# Top 18 by share of GDP
top = sorted(recent, key=lambda r: -r["value"])[:18]

chart_data = [
    {"n": r["countryName"], "v": round(r["value"], 2), "y": r["year"]}
    for r in top
]

if __name__ == "__main__":
    print(json.dumps(chart_data, separators=(",", ":")))
