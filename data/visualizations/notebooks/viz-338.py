# viz-338: Democratic Backsliding 2000-2025
# Dataset: owid--1209753 (V-Dem Electoral Democracy Index, 0-1)

import json
from pathlib import Path

dataset_path = Path(__file__).resolve().parents[2] / "catalog" / "datasets" / "owid--1209753.json"
raw = json.loads(dataset_path.read_text())
data = [r for r in raw["data"] if r["value"] is not None and r["year"] >= 2000]

# Focus countries: major decliners (red), stable references (gray), notable riser (green)
focus = {
    # decliners
    "India": "decline",
    "Hungary": "decline",
    "Turkey": "decline",
    "Hong Kong": "decline",
    "El Salvador": "decline",
    "Venezuela": "decline",
    # stable / reference
    "Sweden": "stable",
    "United States": "stable",
    # riser
    "Sri Lanka": "rise",
}

filtered = [r for r in data if r["countryName"] in focus]
chart_data = sorted(
    [
        {
            "n": r["countryName"],
            "y": r["year"],
            "v": round(r["value"], 3),
            "g": focus[r["countryName"]],
        }
        for r in filtered
    ],
    key=lambda r: (r["n"], r["y"]),
)

if __name__ == "__main__":
    print(json.dumps(chart_data, separators=(",", ":")))
