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
        # Natural Resources Rents as % of GDP — Methodology

        Trend lines showing resource dependency (oil, gas, coal, minerals) as a
        share of GDP for the most resource-dependent economies, revealing boom-bust cycles.
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
            countries[name][year] = round(val, 1)

    selected_names = ['Iraq', 'Equatorial Guinea', 'Congo, Rep.', 'Angola',
                      'Iran, Islamic Rep.', 'Azerbaijan', 'Gabon', 'Kazakhstan']
    name_map = {'Iran, Islamic Rep.': 'Iran', 'Congo, Rep.': 'Congo (Rep.)'}

    print("Resource dependency summary (2019/2020 values):")
    for name in selected_names:
        if name in countries:
            ydata = countries[name]
            v = ydata.get(2019) or ydata.get(2020)
            peak = max(ydata.values())
            print(f"  {name}: latest={v}%, peak={peak}%")
    return countries, selected_names, name_map, AGGREGATES


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows the cyclical boom-bust pattern over 40 years
        - **Country selection**: 8 most resource-dependent nations spanning Middle East, Africa, Central Asia
        - **Time range**: 1980–2021 (captures multiple oil price cycles)
        - **Annotations**: Key crash years (1986, 1998, 2008, 2015) marked with dashed lines
        - **Highlights**: Equatorial Guinea peaked at 88.6% in 2000; Iraq sustained >40% for two decades
        - **Story**: Oil price cycles create extreme GDP volatility for resource-dependent states
        """
    )
    return


@app.cell
def _(json, countries, selected_names, name_map):
    series = []
    for name in selected_names:
        if name in countries:
            ydata = countries[name]
            short = name_map.get(name, name)
            pts = [{'y': yr, 'v': ydata[yr]} for yr in range(1980, 2022) if yr in ydata]
            if len(pts) >= 15:
                series.append({'n': short, 'pts': pts})
    series.sort(key=lambda x: -x['pts'][-1]['v'] if x['pts'] else 0)
    print(json.dumps(series, separators=(',', ':')))
    return (series,)


if __name__ == "__main__":
    app.run()
