# viz-338: A Generation of Forest Loss
# Dataset: wb--AG-LND-FRST-ZS (Forest area, % of land area)
#
# Story: Some countries shed enormous shares of forest cover between
# 1990 and 2023 - Cambodia, Indonesia, and Cote d'Ivoire each lost
# around 17 percentage points of land to other uses. Meanwhile, a
# handful (Bhutan, China, Cuba, Vietnam, Italy) reforested.

import json
from pathlib import Path

dataset_path = Path(__file__).resolve().parents[2] / "catalog" / "datasets" / "wb--AG-LND-FRST-ZS.json"
raw = json.loads(dataset_path.read_text())
data = [r for r in raw["data"] if r["value"] is not None]

# Aggregate country codes used by the World Bank
AGGREGATE_CODES = {
    "1A", "1W", "4E", "7E", "8S", "B8", "EU", "F1", "OE",
    "S1", "S2", "S3", "S4", "T2", "T3", "T4", "T5", "T6", "T7",
    "V1", "V2", "V3", "V4", "XC", "XD", "XE", "XF", "XG",
    "XH", "XI", "XJ", "XL", "XM", "XN", "XO", "XP", "XQ",
    "XT", "Z4", "Z7", "ZF", "ZG", "ZH", "ZI", "ZJ", "ZQ", "ZT",
}
data = [r for r in data if r["country"] not in AGGREGATE_CODES]

by = {}
for r in data:
    by.setdefault(r["countryName"], []).append(r)

records = []
for n, rows in by.items():
    rows = sorted(rows, key=lambda r: r["year"])
    early = next((r for r in rows if r["year"] == 1990), None)
    late = next((r for r in reversed(rows) if r["year"] >= 2018), None)
    if not early or not late:
        continue
    records.append({
        "n": n,
        "v0": round(early["value"], 1),
        "y0": early["year"],
        "v1": round(late["value"], 1),
        "y1": late["year"],
        "d": round(late["value"] - early["value"], 1),
    })

# 8 biggest losers + 6 biggest gainers (skip very small territories)
SKIP_GAINERS = {"Cabo Verde", "Guam"}
losers = sorted(records, key=lambda x: x["d"])[:8]
gainers_all = [g for g in sorted(records, key=lambda x: -x["d"]) if g["n"] not in SKIP_GAINERS]
gainers = gainers_all[:6]

selected = losers + gainers
chart_data = sorted(selected, key=lambda x: x["d"])

if __name__ == "__main__":
    print(json.dumps(chart_data, separators=(",", ":")))
