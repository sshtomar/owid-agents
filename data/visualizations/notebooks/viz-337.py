# viz-337: The Gender Gap in Life Expectancy
# Datasets:
#   wb--SP-DYN-LE00-FE-IN (Life expectancy at birth, female)
#   wb--SP-DYN-LE00-MA-IN (Life expectancy at birth, male)
#
# Story: Women outlive men nearly everywhere - but the size of the gap
# varies enormously. In post-Soviet states it can exceed 9 years; in parts
# of South Asia, North Africa, and the Gulf the gap is barely 3 years.

import json
from pathlib import Path

ds_dir = Path(__file__).resolve().parents[2] / "catalog" / "datasets"
fe = json.loads((ds_dir / "wb--SP-DYN-LE00-FE-IN.json").read_text())["data"]
ma = json.loads((ds_dir / "wb--SP-DYN-LE00-MA-IN.json").read_text())["data"]

# WB aggregate country codes (region/income groups). Country-level data uses ISO-2.
AGGREGATE_CODES = {
    "1A", "1W", "4E", "7E", "8S", "B8", "EU", "F1", "OE",
    "S1", "S2", "S3", "T2", "T3", "T4", "T5", "T6", "T7",
    "V1", "V2", "V3", "V4", "XC", "XD", "XE", "XF", "XG",
    "XH", "XI", "XJ", "XL", "XM", "XN", "XO", "XP", "XQ",
    "XT", "Z4", "Z7", "ZF", "ZH", "ZI", "ZJ", "ZQ", "ZT",
}

YR = 2023

def latest_for_year(rows, year):
    return {
        r["countryName"]: r["value"]
        for r in rows
        if r["year"] == year and r["value"] is not None
        and r["country"] not in AGGREGATE_CODES
    }

fe_yr = latest_for_year(fe, YR)
ma_yr = latest_for_year(ma, YR)

merged = []
for n in (set(fe_yr) & set(ma_yr)):
    f, m = fe_yr[n], ma_yr[n]
    merged.append({"n": n, "f": round(f, 1), "m": round(m, 1),
                    "gap": round(f - m, 1), "y": YR})

merged.sort(key=lambda x: x["gap"])

# Pick 18 countries: 6 smallest gaps, 6 from middle, 6 largest gaps
small = merged[:6]
mid_idx = len(merged) // 2
middle = merged[mid_idx - 3 : mid_idx + 3]
large = merged[-6:]

selected = small + middle + large
# de-dupe in case of overlap
seen = set()
unique = []
for r in selected:
    if r["n"] not in seen:
        unique.append(r)
        seen.add(r["n"])

# Sort the final list by gap ascending so chart reads top-down small->large
chart_data = sorted(unique, key=lambda x: x["gap"])

if __name__ == "__main__":
    print(json.dumps(chart_data, separators=(",", ":")))
