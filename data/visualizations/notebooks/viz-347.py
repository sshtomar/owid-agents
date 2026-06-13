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
        # Maternal Mortality Progress 1990-2023 -- Methodology

        Slope chart showing how maternal mortality ratios changed in the
        25 highest-burden countries between 1990 and 2023.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-STA-MMRT.json"
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
    y1990 = {r['country']:r for r in data if r['year']==1990 and r['country'] not in agg_codes and r['value'] is not None}
    y2023 = {r['country']:r for r in data if r['year']==2023 and r['country'] not in agg_codes and r['value'] is not None}
    common = set(y1990.keys()) & set(y2023.keys())
    rows = sorted([
        {'n': y1990[c]['countryName'], 'a': int(y1990[c]['value']), 'b': int(y2023[c]['value'])}
        for c in common
    ], key=lambda x: -x['a'])[:25]
    print(f"Selected {len(rows)} countries")
    return agg_codes, common, rows, y1990, y2023


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart -- best for showing before/after at two time points
        - **Country selection**: Top 25 by 1990 maternal mortality rate (highest burden)
        - **Time range**: 1990 to 2023 (33-year horizon captures the MDG/SDG era)
        - **Color**: Diverging scale by percent improvement -- deep green for 70%+, red for <20%
        - **Story**: Most countries made dramatic progress; Chad and CAR still lag far behind
        """
    )
    return


@app.cell
def _(json, rows):
    print(json.dumps(rows, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
