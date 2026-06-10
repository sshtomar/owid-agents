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
        # Crop Production Index — Methodology

        Six decades of agricultural productivity growth across 10 countries.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--AG-PRD-CROP-XD.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    exclude_kw = ["income", "World", "Africa", "Asia", "Europe", "OECD", "Pacific",
                  "Caribbean", "North America", "Latin", "Small", "dividend",
                  "fragile", "blend", "IDA", "IBRD", "Arab", "East Asia",
                  "South Asia", "Sub-Saharan", "Euro", "Middle East", "states",
                  "Saharan", "HIPC", "Indebted", "situations", "Other"]
    filtered = [d for d in data if d["value"] is not None
                and not any(x in d["countryName"] for x in exclude_kw)]
    print(f"After filtering: {len(filtered)} rows")
    return (filtered,)


@app.cell
def _(filtered):
    values = [d["value"] for d in filtered]
    countries = sorted(set(d["countryName"] for d in filtered))
    years = sorted(set(d["year"] for d in filtered))
    print(f"Countries: {len(countries)}, Year range: {years[0]}-{years[-1]}")
    print(f"Value range: {min(values):.1f} - {max(values):.1f}")
    return countries, values, years


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows long-run growth trajectories indexed to 2014-2016
        - **Country selection**: Mix of major agricultural producers and stagnators
        - **Time range**: Every 5 years 1961–2022 (reduces data volume while preserving trends)
        - **Highlights**: China 8× growth since 1961; Japan declining; Australia volatile but trending up
        """
    )
    return


@app.cell
def _(json, filtered):
    countries_map = {}
    for r in filtered:
        countries_map.setdefault(r["countryName"], {})[r["year"]] = r["value"]

    SELECTED = ["China", "India", "Brazil", "Indonesia", "Bangladesh",
                "Argentina", "Australia", "France", "Germany", "Japan"]

    chart_data = []
    for name in SELECTED:
        if name not in countries_map:
            continue
        pts_dict = countries_map[name]
        pts = [(y, v) for y, v in sorted(pts_dict.items()) if y % 5 == 0 or y == 2022]
        chart_data.append({
            "n": name,
            "pts": [{"y": y, "v": round(v, 1)} for y, v in pts]
        })

    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
