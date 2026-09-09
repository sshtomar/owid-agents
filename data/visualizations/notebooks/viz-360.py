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
        # Gross Savings Rate: Who Is Saving More? 2000 vs 2023 -- Methodology

        Slope chart comparing gross savings as % of GDP between 2000 and 2023
        for a diverse set of economies, revealing which countries have increased
        or decreased their saving rate.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--NY-GNS-ICTR-ZS.json"
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
    SELECTED = ['CN', 'KR', 'JP', 'BD', 'ID', 'DK', 'CA', 'FR', 'DE', 'AU', 'GR', 'IN', 'GH', 'BR']
    y2000 = {x['country']: x['value'] for x in data if x['year'] == 2000 and x['country'] not in WB_AGGREGATES and x['value'] is not None}
    y2023 = {x['country']: x['value'] for x in data if x['year'] == 2023 and x['country'] not in WB_AGGREGATES and x['value'] is not None}
    names = {x['country']: x['countryName'] for x in data}

    LABELS = {'KR': 'South Korea', 'BD': 'Bangladesh', 'ID': 'Indonesia', 'DK': 'Denmark',
              'CA': 'Canada', 'FR': 'France', 'DE': 'Germany', 'AU': 'Australia',
              'GR': 'Greece', 'IN': 'India', 'GH': 'Ghana', 'BR': 'Brazil',
              'CN': 'China', 'JP': 'Japan'}

    slope = []
    for code in SELECTED:
        if code in y2000 and code in y2023:
            a = round(y2000[code], 1)
            b = round(y2023[code], 1)
            slope.append({'n': LABELS.get(code, names.get(code, code)), 'a': a, 'b': b})

    slope.sort(key=lambda x: -x['a'])
    for s in slope:
        print(f"  {s['n']}: {s['a']}% -> {s['b']}% ({s['b']-s['a']:+.1f}pp)")
    return slope, y2000, y2023, names, WB_AGGREGATES, SELECTED, LABELS


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart (2000 vs 2023) colored by direction and magnitude
        - **Story**: China, Indonesia, Bangladesh, Denmark, India, Germany all raised
          savings rates significantly. Greece collapsed from 20% to 9% (debt crisis).
          Ghana fell from 15% to 9%. Japan and South Korea are stable high savers.
        """
    )
    return


@app.cell
def _(json, slope):
    print(json.dumps(slope, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
