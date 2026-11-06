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
        # Agricultural Land Under Irrigation -- Methodology

        Shows which countries depend most heavily on irrigation, revealing
        where agriculture is most vulnerable to water scarcity.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--AG-LND-IRIG-AG-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict
    by_country = defaultdict(dict)
    for x in data:
        if x["value"] is not None:
            by_country[x["countryName"]][x["year"]] = round(x["value"], 1)

    skip_patterns = ["income", "region", "World", "Europe", "Africa", "Asia",
                     "Americas", "America", "OECD", "fragile", "small", "IDA",
                     "IBRD", "Central", "East", "Latin", "South", "Sub-"]

    latest = {}
    for c, ymap in by_country.items():
        if any(p.lower() in c.lower() for p in skip_patterns):
            continue
        pts = sorted(ymap.items(), reverse=True)
        if pts:
            latest[c] = pts[0]

    top25 = sorted(latest.items(), key=lambda x: x[1][1], reverse=True)[:25]
    print("Top 25 irrigated land countries:")
    for c, (y, v) in top25:
        print(f"  {c} ({y}): {v}%")
    return (top25,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Horizontal bar chart -- best for ranked cross-country comparison
        - **Country selection**: Top 25 by share of agricultural land under irrigation
        - **Data year**: Latest available per country (mostly 2024)
        - **Story**: Egypt irrigates 100% of its farmland -- impossible to farm without
          water infrastructure. Bangladesh at 89%, Israel at 35%. These countries
          face extreme exposure to water shortages.
        """
    )
    return


@app.cell
def _(json, top25):
    name_map = {
        "Egypt, Arab Rep.": "Egypt",
        "Iran, Islamic Rep.": "Iran",
        "Brunei Darussalam": "Brunei"
    }
    chart_data = []
    for c, (y, v) in top25:
        n = name_map.get(c, c)
        chart_data.append({"n": n, "v": v, "y": y})
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
