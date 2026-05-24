# viz-337: The Most Dangerous Roads in the World (2021)
# Dataset: who--RS_198 (estimated road traffic death rate per 100k)
# WHO data uses ISO3 codes; build a name map from owid--1210090 (happiness)
# and owid--1209753 (democracy), which carry full readable country names.

import json
from pathlib import Path

catalog = Path(__file__).resolve().parents[2] / "catalog" / "datasets"
deaths_raw = json.loads((catalog / "who--RS_198.json").read_text())

# Build ISO -> readable name from two well-named OWID datasets
name_map = {}
for src in ("owid--1210090.json", "owid--1209753.json"):
    src_raw = json.loads((catalog / src).read_text())
    for r in src_raw["data"]:
        name_map.setdefault(r["country"], r["countryName"])

# Manual additions for ISO codes not in either source
name_map.update({
    "BLZ": "Belize", "BTN": "Bhutan", "BRN": "Brunei", "CPV": "Cabo Verde",
    "COK": "Cook Islands", "DMA": "Dominica", "GNQ": "Equatorial Guinea",
    "ERI": "Eritrea", "SWZ": "Eswatini", "FSM": "Micronesia", "GAB": "Gabon",
    "GRD": "Grenada", "KIR": "Kiribati", "PRK": "North Korea", "LSO": "Lesotho",
    "MHL": "Marshall Islands", "MAC": "Macao", "MDV": "Maldives", "MCO": "Monaco",
    "NRU": "Nauru", "NIU": "Niue", "PLW": "Palau", "PNG": "Papua New Guinea",
    "PRI": "Puerto Rico", "QAT": "Qatar", "KNA": "St. Kitts and Nevis",
    "LCA": "Saint Lucia", "VCT": "St. Vincent and the Grenadines",
    "WSM": "Samoa", "SMR": "San Marino", "STP": "Sao Tome and Principe",
    "SYC": "Seychelles", "SLB": "Solomon Islands", "SSD": "South Sudan",
    "SUR": "Suriname", "SYR": "Syria", "TLS": "Timor-Leste", "TON": "Tonga",
    "TKM": "Turkmenistan", "TUV": "Tuvalu", "VEN": "Venezuela", "VUT": "Vanuatu",
    "AND": "Andorra", "ATG": "Antigua and Barbuda", "BHS": "Bahamas",
    "BRB": "Barbados", "OMN": "Oman", "PSE": "Palestine",
})

rows = []
for r in deaths_raw["data"]:
    iso = r["country"]
    name = name_map.get(iso, iso)
    rows.append({"n": name, "iso": iso, "v": round(r["value"], 1)})

# Top 25 by death rate (most dangerous) + reference set of major safe countries
sorted_rows = sorted(rows, key=lambda x: -x["v"])
top25 = sorted_rows[:25]
reference_iso = {"SWE", "GBR", "NOR", "JPN", "DEU", "AUS", "USA", "ESP", "FRA"}
reference = [r for r in sorted_rows if r["iso"] in reference_iso]
# Tag each with its group for coloring
for r in top25:
    r["g"] = "danger"
for r in reference:
    r["g"] = "ref"
chart_data = top25 + sorted(reference, key=lambda x: -x["v"])

if __name__ == "__main__":
    print(json.dumps(chart_data, separators=(",", ":")))
