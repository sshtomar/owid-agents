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
        # International Tourism Arrivals, 1995–2020 — Methodology

        Documents the data pipeline for viz-357.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--ST-INT-ARVL.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    selected_countries = {"Italy", "Germany", "Greece", "Japan", "India", "Indonesia", "Croatia", "Austria", "Korea, Rep."}
    filtered = [d for d in data if d["value"] is not None and d["countryName"] in selected_countries]
    print(f"Filtered to {len(filtered)} rows for 9 countries")
    return (filtered,)


@app.cell
def _(filtered):
    from collections import defaultdict
    by_country = defaultdict(dict)
    for row in filtered:
        by_country[row["countryName"]][row["year"]] = row["value"]

    years = list(range(1995, 2021))
    name_map = {"Korea, Rep.": "S. Korea"}
    series = []
    for country, yrs in by_country.items():
        vals = [round(yrs.get(y, 0) / 1e6, 2) if yrs.get(y) else None for y in years]
        if sum(1 for v in vals if v) >= 20:
            series.append({"n": name_map.get(country, country), "s": vals, "y0": 1995})

    print(f"Countries with sufficient data: {len(series)}")
    for s in series:
        non_null = [v for v in s["s"] if v]
        print(f"  {s['n']}: {non_null[0]:.1f}M (1995) -> {non_null[-1]:.1f}M (last)")
    return (series,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows how each country's arrivals evolved over 26 years
        - **Country selection**: 9 countries spanning Europe and Asia; all major destination categories
        - **Time range**: 1995–2020 captures the full growth cycle and COVID-19 collapse
        - **Highlights**: COVID collapsed 2020 arrivals by 50–90%; Japan's growth from 3M to 32M; Italy's scale
        - **COVID annotation**: Shaded band in 2020 with label draws attention to the collapse
        """
    )
    return


@app.cell
def _(json, series):
    print(json.dumps(series, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
