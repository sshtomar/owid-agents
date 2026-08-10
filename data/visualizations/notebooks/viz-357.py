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
    # Old-Age Dependency Ratio — Methodology

    Documents the data pipeline behind viz-357.
    """)
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-POP-DPND-OL.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    filtered = [d for d in data if d["value"] is not None]
    print(f"After filtering nulls: {len(filtered)} rows")
    return (filtered,)


@app.cell
def _(filtered):
    countries_select = {"JP", "IT", "DE", "FR", "CA", "KR", "CN", "BR", "IN", "TD"}
    subset = [d for d in filtered if d["country"] in countries_select]
    values = [d["value"] for d in subset]
    years = sorted(set(d["year"] for d in subset))
    print(f"Countries: {len(set(d['country'] for d in subset))}, Year range: {years[0]}-{years[-1]}")
    print(f"Value range: {min(values):.1f} - {max(values):.1f}")
    return countries_select, subset, values, years


@app.cell
def _(mo):
    mo.md("""
    ## Design Rationale

    - **Chart type**: Trend lines — shows diverging trajectories across 64 years
    - **Country selection**: Japan (highest, ~51), Western Europe (mid-high), Korea and China (accelerating), Brazil/India/Chad (low)
    - **Time range**: 1960–2024, full series
    - **Highlights**: Japan's dramatic rise from 9% to 51%, China's accelerating aging, Chad's persistent youth dependency
    """)
    return


@app.cell
def _(json, subset):
    label_map = {"JP": "Japan", "IT": "Italy", "DE": "Germany", "FR": "France",
                 "CA": "Canada", "KR": "Korea", "CN": "China", "BR": "Brazil",
                 "IN": "India", "TD": "Chad"}
    by_country = {}
    for d in subset:
        c = d["country"]
        if c not in by_country:
            by_country[c] = []
        by_country[c].append(d)

    chart_data = []
    for code, rows in by_country.items():
        rows_sorted = sorted(rows, key=lambda x: x["year"])
        chart_data.append({
            "n": label_map[code],
            "s": [round(r["value"], 2) for r in rows_sorted],
            "y0": rows_sorted[0]["year"]
        })
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
