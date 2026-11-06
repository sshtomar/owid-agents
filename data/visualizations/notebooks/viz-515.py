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
        # New Business Formation Growth -- Methodology

        Shows how new business registrations have grown since 2010 in
        eight major economies, indexed to 2010 = 100.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--IC-BUS-NREG.json"
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
            by_country[x["countryName"]][x["year"]] = x["value"]
    countries_with_2010 = [c for c, m in by_country.items() if 2010 in m and (2022 in m or 2023 in m)]
    print(f"Countries with 2010 and recent data: {len(countries_with_2010)}")
    return (by_country,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Indexed trend lines (2010=100) -- normalizes for country size,
          showing relative growth rather than absolute business counts
        - **Country selection**: 8 economies representing different growth trajectories
        - **Time range**: 2010-2023 -- post-financial-crisis era
        - **Story**: Japan saw 5x growth in new business formation (largely driven by
          simplified registration processes). Chile tripled. Germany barely grew.
          COVID (2020) caused a brief dip in some countries, then strong recovery.
        """
    )
    return


@app.cell
def _(json, by_country):
    targets = ["Brazil", "India", "Germany", "France", "Australia", "China", "Chile", "Japan"]
    chart_data = []
    for c in targets:
        if c not in by_country:
            continue
        ymap = by_country[c]
        if 2010 not in ymap:
            continue
        base = ymap[2010]
        series = []
        for y in range(2010, 2024):
            if y in ymap:
                series.append(round(ymap[y] / base * 100, 1))
            else:
                series.append(None)
        chart_data.append({"n": c, "s": series, "y0": 2010})
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
