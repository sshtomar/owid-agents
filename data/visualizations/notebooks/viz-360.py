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
    mo.md("""
    # Antiretroviral Therapy Coverage — Methodology

    Documents the data pipeline behind viz-360.
    """)
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
    filtered = [d for d in data if d["value"] is not None]
    regions = [
        "Africa Eastern and Southern",
        "Sub-Saharan Africa",
        "Africa Western and Central",
        "Latin America & Caribbean",
        "World",
        "Arab World"
    ]
    subset = [d for d in filtered if d["countryName"] in regions]
    values = [d["value"] for d in subset]
    years = sorted(set(d["year"] for d in subset))
    print(f"Regions: {len(set(d['countryName'] for d in subset))}, Year range: {years[0]}-{years[-1]}")
    print(f"Value range: {min(values):.1f} - {max(values):.1f}%")
    return regions, subset, values, years


@app.cell
def _(mo):
    mo.md("""
    ## Design Rationale

    - **Chart type**: Trend lines — shows the dramatic ART scale-up from 2000 to 2024
    - **Country selection**: Regional aggregates that show geographic variation in access
    - **Time range**: 2000–2024 (full available range)
    - **Highlights**: Eastern/Southern Africa went from 0.2% to 84% in 24 years — the fastest healthcare scale-up in history. Arab World lags at 49%.
    """)
    return


@app.cell
def _(json, subset):
    label_map = {
        "Africa Eastern and Southern": "E+S Africa",
        "Sub-Saharan Africa": "Sub-Saharan Africa",
        "Africa Western and Central": "W+C Africa",
        "Latin America & Caribbean": "Latin America",
        "World": "World",
        "Arab World": "Arab World"
    }
    by_region = {}
    for d in subset:
        r = d["countryName"]
        if r not in by_region:
            by_region[r] = []
        by_region[r].append(d)

    chart_data = []
    for region, rows in by_region.items():
        rows_sorted = sorted(rows, key=lambda x: x["year"])
        chart_data.append({
            "n": label_map[region],
            "s": [round(r["value"], 1) for r in rows_sorted],
            "y0": rows_sorted[0]["year"]
        })
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
