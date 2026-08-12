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
        # Natural Resources Rents as % of GDP, 1990–2021 — Methodology

        Documents the data pipeline for viz-359.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--NY-GDP-TOTL-RT-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    selected = {"Iraq", "Angola", "Kazakhstan", "Azerbaijan", "Algeria", "Bolivia", "Ecuador", "Australia", "Canada"}
    by_country = {}
    for p in data:
        if p["countryName"] in selected and p["value"] is not None:
            c = p["countryName"]
            if c not in by_country:
                by_country[c] = {}
            by_country[c][p["year"]] = p["value"]

    years = list(range(1990, 2022))
    series = []
    for c in sorted(selected):
        if c not in by_country:
            continue
        vals = [round(by_country[c].get(y), 2) if by_country[c].get(y) is not None else None for y in years]
        non_null = sum(1 for v in vals if v is not None)
        if non_null >= 25:
            series.append({"n": c, "s": vals, "y0": 1990})

    print(f"Countries with sufficient data: {len(series)}")
    for s in series:
        vals = [v for v in s["s"] if v is not None]
        print(f"  {s['n']}: max={max(vals):.1f}%, recent={vals[-1]:.1f}%")
    return (series,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows commodity price cycles clearly
        - **Country selection**: Major oil/gas/mineral exporters + diversified economies for contrast
        - **Time range**: 1990–2021; captures 2000s boom, 2014 crash, and post-COVID recovery
        - **Highlights**: Iraq peaks >65% during Gulf War oil prices; commodity cycle visible in all resource states
        - **Annotations**: Oil boom (~2000s) and oil crash (~2014) marked with dashed lines
        """
    )
    return


@app.cell
def _(json, series):
    print(json.dumps(series, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
