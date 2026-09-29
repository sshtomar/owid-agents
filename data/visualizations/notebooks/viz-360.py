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
        # Adjusted Net Savings by Country -- Methodology

        This notebook documents the data pipeline behind viz-360, a trend lines chart
        showing adjusted net savings as % of GNI. Adjusted net savings accounts for
        depreciation of produced capital, depletion of natural resources, and damage
        from pollution — a measure of genuine national wealth creation.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--NY-ADJ-SVNG-GN-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    COUNTRIES = ["Congo, Rep.", "Kazakhstan", "Brazil", "Japan",
                 "Germany", "Denmark", "China", "Bangladesh", "India", "Ghana"]
    by_country = {}
    for row in data:
        if row["countryName"] in COUNTRIES and row["value"] is not None:
            by_country.setdefault(row["countryName"], {})[row["year"]] = row["value"]

    for c in COUNTRIES:
        if c in by_country:
            vs = by_country[c]
            years = sorted(vs.keys())
            print(f"  {c}: {years[0]}-{years[-1]}, latest={vs[years[-1]]:.1f}%")
    return COUNTRIES, by_country


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines -- multi-series 1990-2021
        - **Country selection**: Resource-curse cases (Congo, Kazakhstan), declining savers (Brazil),
          stable positive (Germany, Denmark), high-saving developers (Bangladesh, China, India)
        - **Zero reference line** to clearly distinguish positive/negative adjusted savings
        - **Highlights**:
          - Congo: extreme negative values (-30 to -97%) from oil depletion without reinvestment
          - Bangladesh: rising from 11% to 32% -- extraordinary genuine wealth accumulation
          - Brazil: fell from positive into slightly negative
        """
    )
    return


@app.cell
def _(json, COUNTRIES, by_country):
    chart_data = []
    for c in COUNTRIES:
        if c not in by_country:
            continue
        vs = by_country[c]
        y0 = min(vs.keys())
        yend = max(vs.keys())
        series = [round(vs[y], 2) if y in vs else None for y in range(y0, yend + 1)]
        label = c.replace("Congo, Rep.", "Congo")
        chart_data.append({"n": label, "s": series, "y0": y0})
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
