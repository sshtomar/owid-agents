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
        # International Tourism Arrivals 2005-2020 -- Methodology

        Tracks international tourist arrivals for major destination countries,
        culminating in the dramatic COVID-19 collapse in 2020.
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
    from collections import defaultdict
    by_country = defaultdict(dict)
    for row in data:
        if row["value"] is not None:
            by_country[row["countryName"]][row["year"]] = row["value"]

    target = ["France", "China", "Italy", "Germany", "Austria", "Japan"]
    years = list(range(2005, 2021))

    chart_data = []
    for country in target:
        if country in by_country:
            vals = by_country[country]
            series = [round(vals[y] / 1e6, 2) if y in vals else None for y in years]
            if all(v is not None for v in series):
                chart_data.append({"n": country, "s": series, "y0": 2005, "step": 1})

    print(f"Countries: {[d['n'] for d in chart_data]}")
    print(f"Year range: {years[0]}-{years[-1]}")
    return chart_data, by_country, target, years


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
