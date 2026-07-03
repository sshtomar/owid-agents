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
        # International Tourism Arrivals: COVID Collapse — Methodology

        Trend lines showing international visitor arrivals (millions) for the top 10
        destinations, revealing the unprecedented 2020 COVID collapse.
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
    print(f"Year range: {meta['dateRange']['start']} - {meta['dateRange']['end']}")
    return data, meta, raw


@app.cell
def _(data):
    AGGREGATES = {'XD','XM','XN','XO','XP','XQ','XJ','XT','XS','XR','OE','EU','ZH','ZG','ZF','ZI',
                  '1A','1W','4E','7E','8S','B8','ZT','ZJ','ZL','ZQ','ZU','V1','V2','V3','V4',
                  'XC','XE','XL','XU','XY','YI','W6','S3','S1','S2','S4','T4','T5','T6','T7',
                  'XF','XG','XI'}
    countries = {}
    for pt in data:
        code = pt['country']
        name = pt['countryName']
        year = pt['year']
        val = pt['value']
        if val is not None and len(code) == 2 and code.isalpha() and code not in AGGREGATES:
            if name not in countries:
                countries[name] = {}
            countries[name][year] = round(val / 1e6, 1)

    top_with_2020 = [(n, y.get(2019), y) for n, y in countries.items() if y.get(2019) and y.get(2020)]
    top_with_2020.sort(key=lambda x: -x[1])
    top10 = [n for n, v, y in top_with_2020[:10]]
    print("Top 10 by 2019 arrivals with 2020 data:")
    for n, v, y in top_with_2020[:10]:
        drop = round((y.get(2020) - v) / v * 100)
        print(f"  {n}: {v:.1f}M → {y.get(2020):.1f}M ({drop:+}%)")
    return countries, top10, AGGREGATES, top_with_2020


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows temporal evolution and COVID collapse most clearly
        - **Country selection**: Top 10 destinations that also have 2020 data (to show the COVID drop)
        - **Time range**: 2000–2020 (full time series available)
        - **Color encoding**: Warm-to-cool palette by 2019 rank
        - **Highlights**: Hong Kong -94%, China -81%, Japan -87% vs France -46% (less severe)
        - **Annotation**: COVID-19 vertical dashed line at 2020, drop % shown in endpoint labels
        """
    )
    return


@app.cell
def _(json, countries, top10):
    name_map = {'Hong Kong SAR, China': 'Hong Kong', 'Korea, Rep.': 'South Korea'}
    series = []
    for name in top10:
        ydata = countries[name]
        short = name_map.get(name, name)
        pts = [{'y': yr, 'v': ydata[yr]} for yr in range(2000, 2021) if yr in ydata]
        if len(pts) >= 10:
            series.append({'n': short, 'pts': pts})
    series.sort(key=lambda x: -x['pts'][-2]['v'])
    print(json.dumps(series, separators=(',', ':')))
    return (series,)


if __name__ == "__main__":
    app.run()
