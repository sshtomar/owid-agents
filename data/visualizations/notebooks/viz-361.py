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
        # Cereal Yield, 1961–2022 — Methodology

        Documents the data pipeline for viz-361.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--AG-YLD-CREL-KG.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    selected = {"China", "India", "Germany", "France", "Brazil", "Argentina", "Japan", "Korea, Rep.", "Ethiopia"}
    name_map = {"Korea, Rep.": "S. Korea"}
    by_country = {}
    for p in data:
        if p["countryName"] in selected and p["value"] is not None:
            c = p["countryName"]
            if c not in by_country:
                by_country[c] = {}
            by_country[c][p["year"]] = p["value"]

    years = list(range(1961, 2023))
    series = []
    for c in sorted(selected):
        if c not in by_country:
            continue
        vals = [round(by_country[c].get(y)) if by_country[c].get(y) is not None else None for y in years]
        non_null = sum(1 for v in vals if v is not None)
        if non_null >= 50:
            series.append({"n": name_map.get(c, c), "s": vals, "y0": 1961})

    print(f"Countries: {len(series)}")
    for s in series:
        vals = [v for v in s["s"] if v]
        print(f"  {s['n']}: {vals[0]:,} -> {vals[-1]:,} kg/ha ({vals[-1]/vals[0]:.1f}x)")
    return (series,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — 62-year time series shows agricultural transformation
        - **Country selection**: Major producers spanning continents + Ethiopia as low-yield contrast
        - **Highlights**: China grew from 1,193 to 6,381 kg/ha (5.3x); Germany leads at 7,126; Ethiopia doubled but still trails far behind
        - **Annotation**: Green Revolution (~1966) marked as inflection point
        - **Story**: Divergence between high-input industrial farming and smallholder-dependent regions is stark
        """
    )
    return


@app.cell
def _(json, series):
    print(json.dumps(series, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
