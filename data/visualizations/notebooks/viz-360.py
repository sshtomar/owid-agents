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
        # Nuclear Electricity Slope Chart — Methodology

        Documents the data pipeline for viz-360: slope chart showing nuclear electricity
        share (% of total) for 16 countries, 2000 vs 2022.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-ELC-NUCL-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    c_2000 = {}
    c_2022 = {}
    for row in data:
        c = row['countryName']
        y = row['year']
        v = row['value']
        if v is None:
            continue
        if y == 2000:
            c_2000[c] = round(v, 1)
        if y == 2022:
            c_2022[c] = round(v, 1)

    both = set(c_2000.keys()) & set(c_2022.keys())
    significant = [(c, c_2000[c], c_2022[c]) for c in both
                   if c_2000.get(c, 0) >= 2 or c_2022.get(c, 0) >= 2]
    significant.sort(key=lambda x: x[2], reverse=True)
    print("Countries with significant nuclear share:")
    for name, v0, v1 in significant:
        print(f"  {name}: {v0}% -> {v1}%")
    return both, c_2000, c_2022, significant


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — two-point (2000 vs 2022) clearly shows direction
        - **Country selection**: All countries with >2% nuclear in either year
        - **Color**: Green = increased share, amber = stable, red = major decline
        - **Story**: Nuclear has diverged sharply. Germany's political decision caused
          a near-phase-out; Japan's Fukushima disaster cut its share from 30% to 5.5%.
          Meanwhile Czechia, Hungary, and Belarus expanded. France dominates at 62%.
        """
    )
    return


@app.cell
def _(json, c_2000, c_2022, significant):
    skip = {'European Union', 'Euro area', 'OECD members'}
    name_map = {'Korea, Rep.': 'South Korea'}
    chart_data = []
    for name, v0, v1 in significant:
        if name in skip:
            continue
        chart_data.append({"n": name_map.get(name, name), "a": v0, "b": v1})
    print(json.dumps(chart_data, separators=(",", ":")))
    return chart_data, name_map, skip
