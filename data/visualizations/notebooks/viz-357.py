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
        # Antiretroviral Therapy Coverage — Methodology

        Visualizes the global scale-up of HIV treatment from 2000 to 2024 across 10 countries
        spanning Sub-Saharan Africa, Southeast Asia, and the Caribbean.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-HIV-ARTC-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict
    by_country = defaultdict(list)
    for pt in data:
        if pt["value"] is not None:
            by_country[pt["countryName"]].append((pt["year"], pt["value"]))
    print(f"Countries with data: {len(by_country)}")
    return by_country, defaultdict


@app.cell
def _(by_country, json):
    selected = ["Botswana","Eswatini","Burundi","Cambodia","Kenya","Ethiopia","Cameroon","Haiti","Ecuador","Cote d'Ivoire"]
    chart_data = []
    for c in selected:
        if c not in by_country:
            continue
        all_pts = {y: v for y, v in by_country[c]}
        series = [all_pts.get(yr) for yr in range(2000, 2025)]
        chart_data.append({"n": c, "s": series, "y0": 2000})
    print(f"Chart data ({len(chart_data)} countries):")
    for row in chart_data:
        vals = [v for v in row["s"] if v is not None]
        print(f"  {row['n']}: {vals[0]:.0f}% -> {vals[-1]:.0f}%")
    print(json.dumps(chart_data, separators=(",", ":")))
    return chart_data, c, selected


if __name__ == "__main__":
    app.run()
