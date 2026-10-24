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
        # Coal Electricity Generation — Methodology

        This notebook documents the data pipeline for viz-511: trend lines of coal
        electricity generation (TWh) for the top 11 producers, 2000–2024.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "ember--GEN-COAL.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict
    by_country = defaultdict(dict)
    for pt in data:
        if pt["value"] is not None:
            by_country[pt["countryName"]][pt["year"]] = pt["value"]

    top_2024 = sorted(
        [(c, v.get(2024, v.get(2023, 0))) for c, v in by_country.items()],
        key=lambda x: -x[1]
    )[:11]
    print("Top 11 coal generators in 2024:")
    for n, v in top_2024:
        print(f"  {n}: {v:.1f} TWh")
    return by_country, top_2024


@app.cell
def _(json, by_country, top_2024):
    name_map = {
        "United States of America": "USA",
        "Russian Federation (the)": "Russia",
        "South Korea": "S. Korea",
        "South Africa": "S. Africa",
        "Viet Nam": "Vietnam",
    }
    years = list(range(2000, 2025))
    chart_data = []
    for name, _ in top_2024:
        display = name_map.get(name, name)
        if name in by_country:
            series = [round(by_country[name].get(y, 0) or 0, 1) for y in years]
            chart_data.append({"n": display, "s": series, "y0": 2000})
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
