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
        # Hydroelectric Power: Who Diversified, 2000 vs 2023 -- Methodology

        Slope chart comparing the share of electricity from hydropower in 2000
        versus 2023 for countries where hydro was historically dominant.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-ELC-HYRO-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    WB_AGGREGATES = {
        '1A','ZH','ZI','S3','B8','V2','Z4','4E','T4','XC','Z7','7E','T7','EU','XE',
        'XD','XF','ZT','XH','XI','XG','V3','ZJ','XJ','T2','XL','XO','XM','XN','ZQ',
        'T3','XQ','XP','XU','OE','S4','S2','V4','V1','S1','8S','T5','ZG','T6','ZF',
        'XT','1W'
    }
    y2000 = {x['country']: x['value'] for x in data if x['year'] == 2000 and x['country'] not in WB_AGGREGATES and x['value'] is not None and x['value'] > 0}
    y2023 = {x['country']: x['value'] for x in data if x['year'] == 2023 and x['country'] not in WB_AGGREGATES and x['value'] is not None}
    names = {x['country']: x['countryName'] for x in data}

    slope = []
    for code in y2000:
        if code in y2023:
            a = y2000[code]
            b = y2023[code]
            if a > 50 or b > 50:
                slope.append({'n': names.get(code, code), 'a': round(a, 1), 'b': round(b, 1)})

    slope.sort(key=lambda x: -x['a'])
    for s in slope:
        print(f"  {s['n']}: {s['a']}% -> {s['b']}% ({s['b']-s['a']:+.1f}pp)")
    return slope, y2000, y2023, names, WB_AGGREGATES


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart (2000 vs 2023) colored by magnitude of decline
        - **Country selection**: Countries where hydro was >50% of electricity in 2000
        - **Story**: Congo DR, Ethiopia, and Albania still get >96% from hydro.
          Ghana and Congo Rep. dropped dramatically (thermal and other sources expanded).
          Brazil fell from 87% to 60% as it diversified into wind and solar.
          Angola is the exception — it increased hydro share by building new capacity.
        """
    )
    return


@app.cell
def _(json, slope):
    print(json.dumps(slope, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
