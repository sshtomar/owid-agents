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
        # When the Planes Stopped -- Methodology

        International tourism arrivals 1995-2020 for 10 countries.
        Source: World Bank ST.INT.ARVL.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--ST-INT-ARVL.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    countries = {}
    for pt in data:
        c = pt["countryName"]
        if c not in countries:
            countries[c] = {}
        if pt["value"] is not None:
            countries[c][str(pt["year"])] = pt["value"]

    selected = ["China","Italy","Germany","Hong Kong SAR, China","Japan",
                "Korea, Rep.","Greece","Australia","Indonesia","Georgia"]
    years = list(range(1995, 2021))
    chart_data = []
    labels = {"Hong Kong SAR, China": "Hong Kong", "Korea, Rep.": "Korea"}
    for c in selected:
        if c in countries:
            series = [round(countries[c].get(str(y), None) / 1e6, 1)
                      if countries[c].get(str(y)) else None for y in years]
            chart_data.append({"n": labels.get(c, c), "s": series})
    print(f"Chart data for {len(chart_data)} countries, {len(years)} years (1995-2020)")
    print(f"Max value: {max(v for d in chart_data for v in d['s'] if v is not None):.1f}M")
    return chart_data, countries, labels, selected, years


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines -- shows long arc of growth and the dramatic 2020 cliff
        - **Country selection**: Mix of top destinations across Asia and Europe with full 1995-2020 data
        - **Y axis**: Millions of international arrivals
        - **Annotation**: Vertical dashed line at 2020 labeled COVID-19
        - **Highlight**: China's explosive growth from 46M to 162M, then fall to 30M
        - **Key insight**: Hong Kong dropped 94%, Japan 87%, Korea 86%
        """
    )
    return


if __name__ == "__main__":
    app.run()
