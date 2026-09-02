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
        # International Tourism Arrivals -- Methodology

        Documents the data pipeline for viz-357: trend lines showing international
        tourist arrivals for 10 major destinations, 1995-2020.
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
    # Filter to selected countries only (ISO 2-letter codes)
    SELECTED = {"FR": "France", "CN": "China", "IT": "Italy", "HR": "Croatia",
                "HK": "Hong Kong", "DE": "Germany", "GR": "Greece",
                "AT": "Austria", "JP": "Japan", "KR": "South Korea"}

    filtered = [d for d in data if d["value"] is not None and d["country"] in SELECTED]
    print(f"Filtered to {len(filtered)} data points across {len(SELECTED)} countries")
    return SELECTED, filtered


@app.cell
def _(SELECTED, filtered):
    # Build per-country year-value maps
    countries = {name: {} for name in SELECTED.values()}
    for pt in filtered:
        name = SELECTED[pt["country"]]
        countries[name][pt["year"]] = round(pt["value"] / 1e6, 2)

    years = list(range(1995, 2021))
    chart_data = []
    for name, yv in countries.items():
        series = [yv.get(y) for y in years]
        while series and series[-1] is None:
            series.pop()
        if yv.get(2019):
            chart_data.append({"n": name, "s": series, "y0": 1995, "step": 1})

    chart_data.sort(key=lambda x: x["s"][-2] if len(x["s"]) >= 2 else 0, reverse=True)
    print(f"Chart series: {len(chart_data)} countries")
    return chart_data, countries, years


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines -- shows multi-country evolution over time with a dramatic endpoint
        - **Country selection**: Top 10 destinations by 2019 arrivals with available data
        - **Time range**: 1995-2020 to capture full growth arc and COVID collapse
        - **Highlights**: France leads, China grew 3.5x from 2000 to 2019, all crashed in 2020
        - **Values**: Millions of arrivals (includes overnight and same-day visitors per World Bank definition)
        """
    )
    return


@app.cell
def _(chart_data, json):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
