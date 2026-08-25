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
        # Fossil Fuel Energy Consumption — Methodology

        Documents the data pipeline behind viz-360.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-USE-COMM-FO-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict
    by_country = defaultdict(dict)
    for x in data:
        if x['value'] is not None and x['value'] > 0:
            by_country[x['countryName']][x['year']] = x['value']
    countries = [
        'Iceland', 'Denmark', 'France', 'Germany', 'China', 'India',
        'Australia', 'Japan', 'Italy', 'Canada', 'Brazil', 'Costa Rica'
    ]
    for c in countries:
        v = by_country.get(c, {})
        if v and v.get(1990) and v.get(2014):
            print(f"{c}: 1990={v[1990]:.1f}%, 2014={v[2014]:.1f}% ({v[2014]-v[1990]:+.1f}%)")
    return by_country, countries


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — 1990–2014 time series
        - **Country selection**: Mix of high and low fossil fuel dependency with diverse trajectories
        - **Time range**: 1990–2014 (data quality drops sharply after 2015 in this series)
        - **Highlights**: Japan's sharp increase after Fukushima (2011); Iceland and Brazil maintain
          low fossil fuel share thanks to geothermal and hydro; China deepened dependency;
          Denmark made steady gains
        """
    )
    return


@app.cell
def _(json, by_country, countries):
    all_years = list(range(1990, 2015))
    chart_data = []
    for c in countries:
        v = by_country.get(c, {})
        if v and v.get(1990) and v.get(2014):
            series = [round(v[y], 1) if y in v and v[y] > 0 else None for y in all_years]
            chart_data.append({"n": c, "s": series, "y0": 1990})
    print(json.dumps(chart_data, separators=(',', ':')))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
