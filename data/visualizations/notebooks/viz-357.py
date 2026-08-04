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
        # Breast Cancer 5-Year Survival Rate, 2021 — Methodology

        Horizontal bar chart comparing breast cancer survival rates across countries,
        split into top-20 and bottom-20 to highlight the global healthcare inequality.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--CANCERSURVIVAL_BREASTCANCER.json"
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
        "NGA": "Nigeria", "ETH": "Ethiopia", "TCD": "Chad", "NER": "Niger",
        "BFA": "Burkina Faso", "MLI": "Mali", "MOZ": "Mozambique",
        "GIN": "Guinea", "SOM": "Somalia", "CAF": "Central African Rep.",
        "LSO": "Lesotho", "SWZ": "Eswatini", "MCO": "Monaco", "AND": "Andorra",
        "GNB": "Guinea-Bissau", "BDI": "Burundi", "COD": "D.R. Congo",
        "TZA": "Tanzania", "UGA": "Uganda", "SSD": "South Sudan",
        "CMR": "Cameroon", "CIV": "Cote d'Ivoire", "BEN": "Benin",
        "SLE": "Sierra Leone", "LBR": "Liberia", "DJI": "Djibouti",
        "COM": "Comoros", "ERI": "Eritrea", "GMB": "Gambia",
    })
    print(f"Name lookup size: {len(name_map)}")
    return (name_map,)


@app.cell
def _(data, name_map):
    regional_skip = {
        "GLOBAL", "AFR", "AMR", "EMR", "EUR", "SEAR", "WPR",
        "WB_HI", "WB_LI", "WB_LMI", "WB_UMI", "LDC", "LLDC", "SIDS",
        "HIC", "LIC", "LMC", "UMC",
    }
    rows = []
    for r in data:
        iso = r["country"]
        if iso in regional_skip or len(iso) != 3 or r["value"] is None:
            continue
        name = name_map.get(iso, iso)
        rows.append({"n": name, "v": round(r["value"], 1), "g": "high" if r["value"] >= 70 else "low"})
    rows.sort(key=lambda x: -x["v"])
    countries_count = len(rows)
    print(f"Countries: {countries_count}")
    print(f"Range: {rows[-1]['v']}% — {rows[0]['v']}%")
    print(f"Top 3: {[(r['n'], r['v']) for r in rows[:3]]}")
    print(f"Bottom 3: {[(r['n'], r['v']) for r in rows[-3:]]}")
    return (rows,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Horizontal bar chart — natural for ranked comparison of many countries
        - **Country selection**: Top 20 (best) + bottom 20 (worst) to tell the inequality story
        - **Color**: Warm (high survival) to cool (low survival) encoding
        - **Key story**: 4x difference between Monaco (94%) and Central African Rep. (25%)
        """
    )
    return


@app.cell
def _(json, rows):
    chart_data = rows[:20] + rows[-20:]
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
