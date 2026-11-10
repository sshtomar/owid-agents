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
        # New Businesses Registered — Methodology

        Sparkline grid showing entrepreneurship trends for top 24 economies by registration count.
        Source dataset: wb--IC-BUS-NREG
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--IC-BUS-NREG.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    country_data = {}
    for p in data:
        if p["value"] is None:
            continue
        cn = p["countryName"]
        yr = p["year"]
        country_data.setdefault(cn, {})[yr] = p["value"]

    skip_words = ["income","Africa","Asia","Europe","America","World","OECD","dividend","Arab","states","IDA","IBRD","South","North","East","West","Central","Caribbean","Euro area","European","Latin","Pacific","Middle"]
    result = {}
    for k, v in country_data.items():
        if any(w in k for w in skip_words):
            continue
        years = sorted(v.keys())
        if len(years) >= 8 and max(years) >= 2020:
            result[k] = v

    top = sorted(result.items(), key=lambda x: x[1].get(2024, x[1].get(2023, 0)), reverse=True)[:24]
    chart_data = []
    for name, vals in top:
        years = sorted(vals.keys())
        series = [round(vals[y]) for y in years]
        chart_data.append({"n": name, "s": series, "y0": years[0], "e": series[0], "l": series[-1]})
        print(f"{name}: {years[0]}-{years[-1]}, {series[0]:,} -> {series[-1]:,}")
    return chart_data, country_data, result, top


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Sparkline grid — 24 countries, each showing full time series compactly
        - **Sorting**: By most recent count (descending) — largest entrepreneurs at top-left
        - **Layout**: 6 columns × 4 rows
        - **Highlights**: Brazil surged 3.4× from 2006 to 2024; Japan started tiny (3,450) and grew 12×
        - **Interactivity**: Crosshair + tooltip on hover showing year and count
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
