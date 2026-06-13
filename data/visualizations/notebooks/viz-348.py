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
        # Road Traffic Mortality, 2000 vs 2019 -- Methodology

        Slope chart comparing road traffic mortality rates (per 100,000 population)
        in 2000 and 2019 for the 25 highest-burden countries in 2000.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-STA-TRAF-P5.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    agg_codes = {'1A','1W','4E','7E','8S','B8','EU','F1','OE','S1','S2','S3','S4',
                 'T2','T3','T4','T5','T6','T7','V1','V2','V3','V4','XC','XD','XE',
                 'XF','XG','XH','XI','XJ','XL','XM','XN','XO','XP','XQ','XT','XU',
                 'Z4','Z7','ZF','ZG','ZH','ZI','ZJ','ZQ','ZT','KP'}
    y2000 = {r['country']:r for r in data if r['year']==2000 and r['country'] not in agg_codes and r['value'] is not None}
    y2019 = {r['country']:r for r in data if r['year']==2019 and r['country'] not in agg_codes and r['value'] is not None}
    common = set(y2000.keys()) & set(y2019.keys())
    rows = sorted([
        {'n': y2000[c]['countryName'], 'a': round(y2000[c]['value'],1), 'b': round(y2019[c]['value'],1)}
        for c in common
    ], key=lambda x: -x['a'])[:25]
    print(f"Selected {len(rows)} countries")
    return agg_codes, common, rows, y2000, y2019


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart -- shows changes between two time points clearly
        - **Country selection**: Top 25 by 2000 rate (highest-burden)
        - **Color**: Rising rates in warm red, falling in green -- direction of change matters
        - **Story**: Dominican Republic saw a dramatic surge; Korea cut its rate by two-thirds
        """
    )
    return


@app.cell
def _(json, rows):
    print(json.dumps(rows, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
