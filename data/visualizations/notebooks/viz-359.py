import marimo

app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import json
    from pathlib import Path
    return json, mo, Path


@app.cell
def _(mo):
    mo.md(
        """
        # Effective Eye Care Coverage, 2023 — Methodology

        Horizontal bar chart showing the percentage of people with refractive
        error receiving effective correction, by country. Reveals the global
        gap in preventable vision loss.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--NCD_SENSORYFUNCTION_VISION_EREC.json"
    raw = json.loads(dataset_path.read_text())
    data = raw["data"]
    print(f"Loaded {len(data)} data points")
    return data, raw


@app.cell
def _(json, mo):
    name_src_1 = mo.notebook_location() / "public" / "catalog" / "datasets" / "owid--1210090.json"
    name_src_2 = mo.notebook_location() / "public" / "catalog" / "datasets" / "owid--1209753.json"
    name_map = {}
    for src in (name_src_1, name_src_2):
        for r in json.loads(src.read_text())["data"]:
            name_map.setdefault(r["country"], r["countryName"])
    name_map.update({
        "NER": "Niger", "BFA": "Burkina Faso", "MLI": "Mali", "TCD": "Chad",
        "SSD": "South Sudan", "ETH": "Ethiopia", "SEN": "Senegal", "GIN": "Guinea",
        "GNB": "Guinea-Bissau", "BEN": "Benin", "BDI": "Burundi", "SLE": "Sierra Leone",
        "SOM": "Somalia", "MOZ": "Mozambique", "CIV": "Cote d'Ivoire",
        "CAF": "Central African Rep.", "RWA": "Rwanda", "ERI": "Eritrea",
        "GMB": "Gambia", "DJI": "Djibouti", "KOR": "South Korea",
        "CHE": "Switzerland", "DNK": "Denmark", "NOR": "Norway",
        "DEU": "Germany", "NLD": "Netherlands", "LUX": "Luxembourg",
        "AND": "Andorra", "ISL": "Iceland", "JPN": "Japan", "LTU": "Lithuania",
        "EST": "Estonia", "VIR": "US Virgin Islands",
    })
    print(f"Name map size: {len(name_map)}")
    return (name_map,)


@app.cell
def _(data, name_map):
    from collections import defaultdict
    regional_skip = {
        "GLOBAL", "AFR", "AMR", "EMR", "EUR", "SEAR", "WPR",
        "WB_HI", "WB_LI", "WB_LMI", "WB_UMI",
    }
    country_vals = defaultdict(list)
    for r in data:
        iso = r["country"]
        if iso in regional_skip or len(iso) != 3 or r["value"] is None:
            continue
        country_vals[iso].append(r["value"])

    rows = []
    for iso, vals in country_vals.items():
        avg = round(sum(vals) / len(vals), 1)
        name = name_map.get(iso, iso)
        if len(name) == 3:
            continue
        rows.append({"n": name, "v": avg})

    rows.sort(key=lambda x: x["v"])
    print(f"Countries with names: {len(rows)}")
    print("Bottom 5:", [(r["n"], r["v"]) for r in rows[:5]])
    print("Top 5:", [(r["n"], r["v"]) for r in rows[-5:]])
    return (rows,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Horizontal bar chart — intuitive ranking of coverage percentage
        - **Country selection**: Bottom 20 (worst access) + top 10 (best access) with gap
        - **Dataset quirk**: 5–6 estimates per country (sex/age disaggregated); averaged for display
        - **Story**: Niger has <17% coverage; Switzerland has >86%. 5× gap for a correctable condition
        """
    )
    return


@app.cell
def _(json, rows):
    chart_data = rows[:20] + rows[-10:]
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
