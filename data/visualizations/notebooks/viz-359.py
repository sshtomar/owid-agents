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
    # Energy Use Per Capita — Methodology

    Documents the data pipeline behind viz-359.
    """)
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-USE-PCAP-KG-OE.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    filtered = [d for d in data if d["value"] is not None]
    codes = {"IS": "Iceland", "CA": "Canada", "AU": "Australia", "KR": "Korea",
             "DE": "Germany", "FR": "France", "CN": "China", "BR": "Brazil",
             "IN": "India", "ID": "Indonesia"}
    subset = [d for d in filtered if d["country"] in codes]
    values = [d["value"] for d in subset]
    years = sorted(set(d["year"] for d in subset))
    print(f"Countries: {len(set(d['country'] for d in subset))}, Year range: {years[0]}-{years[-1]}")
    print(f"Value range: {min(values):.0f} - {max(values):.0f} kg oil equiv./person")
    return codes, subset, values, years


@app.cell
def _(mo):
    mo.md("""
    ## Design Rationale

    - **Chart type**: Trend lines — shows diverging energy intensity trajectories since 1990
    - **Country selection**: Iceland (geothermal outlier), Canada/Australia (high), Germany/France (declining), Korea (rising), China (rapid growth), Brazil/India/Indonesia (emerging)
    - **Time range**: 1990–2024
    - **Highlights**: Iceland's extreme geothermal use, China's near-quadrupling, Germany's ~36% reduction
    """)
    return


@app.cell
def _(json, codes, subset):
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
            "n": codes[code],
            "s": [round(r["value"], 0) for r in rows_sorted],
            "y0": rows_sorted[0]["year"]
        })
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
