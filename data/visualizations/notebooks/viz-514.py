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
        # Rotavirus Vaccine Coverage -- Methodology

        Sparkline grid showing rotavirus vaccine coverage among infants (%) from 2006-2025
        for 30 countries. Shows when each country adopted the vaccine and current coverage.
        Data is forward-filled after first reported non-zero value.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--ROTAC.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data, json):
    iso_to_name = {
        "IND": "India", "NGA": "Nigeria", "PAK": "Pakistan", "ETH": "Ethiopia",
        "DEU": "Germany", "GBR": "UK", "FRA": "France", "ZAF": "S. Africa",
        "GHA": "Ghana", "IDN": "Indonesia", "NOR": "Norway", "SWE": "Sweden",
        "JPN": "Japan", "KOR": "S. Korea", "EGY": "Egypt",
        "ALB": "Albania", "ARM": "Armenia", "NIC": "Nicaragua", "ERI": "Eritrea",
        "SEN": "Senegal", "TGO": "Togo", "NER": "Niger", "ZWE": "Zimbabwe",
        "DOM": "Dominican Rep", "LVA": "Latvia", "CMR": "Cameroon",
        "MOZ": "Mozambique", "KEN": "Kenya", "RWA": "Rwanda", "MAR": "Morocco",
        "COL": "Colombia", "AUT": "Austria", "BEL": "Belgium", "QAT": "Qatar",
        "BDI": "Burundi", "BGD": "Bangladesh", "BOL": "Bolivia",
        "HND": "Honduras", "UZB": "Uzbekistan", "TKM": "Turkmenistan",
        "BWA": "Botswana", "SLE": "Sierra Leone", "SAU": "Saudi Arabia"
    }

    from collections import defaultdict
    by_country = defaultdict(dict)
    for r in data:
        c = r["countryName"]
        if r["value"] is not None:
            by_country[c][r["year"]] = r["value"]

    years = list(range(2006, 2026))

    grid_data = []
    for code in iso_to_name:
        vals = by_country.get(code, {})
        name = iso_to_name[code]
        latest = vals.get(2025, vals.get(2024, vals.get(2023, 0)))
        if latest < 20:
            continue
        series = [vals.get(y, 0) for y in years]
        last_known = 0
        filled = []
        for v in series:
            if v > 0:
                last_known = v
            filled.append(last_known)
        if max(filled) < 20:
            continue
        grid_data.append({"n": name, "s": filled, "latest": filled[-1]})

    grid_data.sort(key=lambda x: x["latest"], reverse=True)
    grid_data = grid_data[:30]

    print(f"Countries in grid: {len(grid_data)}")
    chart_data = [{"n": gd["n"], "s": gd["s"]} for gd in grid_data]
    print(json.dumps(chart_data, separators=(",", ":")))
    return chart_data,


if __name__ == "__main__":
    app.run()
