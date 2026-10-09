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
        # Marine Protected Areas — Methodology

        Slope chart comparing the share of territorial waters under marine protection
        in 2013 vs 2024 for the 20 countries with the highest 2024 levels.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--ER-MRN-PTMR-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    AGGREGATES = {
        'ZH','ZI','1A','S3','B8','V2','Z4','4E','T4','XC','Z7','7E','T7','EU','F2',
        'XE','XD','XF','ZT','XH','XI','XG','V3','ZJ','XJ','T2','XL','XO','XM','XN',
        'ZQ','XQ','T3','XP','XU','OE','S4','S2','V4','V1','S1','8S','T5','ZG','ZF',
        'T6','XT','1W'
    }
    by_country = {}
    for row in data:
        cc = row.get('country', '')
        if cc in AGGREGATES or len(cc) != 2:
            continue
        name = row.get('countryName', '')
        year = row.get('year', 0)
        val = row.get('value')
        if val is None:
            continue
        if cc not in by_country:
            by_country[cc] = {'name': name, 'years': {}}
        by_country[cc]['years'][year] = val

    slope = []
    for cc, info in by_country.items():
        yrs = info['years']
        a = yrs.get(2013) or yrs.get(2014)
        b = yrs.get(2024) or yrs.get(2023)
        if a is not None and b is not None:
            slope.append({'n': info['name'], 'a': round(a, 2), 'b': round(b, 2)})

    chart_data = sorted(slope, key=lambda x: -x['b'])[:20]
    print(f"Countries with both 2013 and 2024 data: {len(slope)}")
    return chart_data, slope, by_country, AGGREGATES


@app.cell
def _(chart_data):
    changes = [d['b'] - d['a'] for d in chart_data]
    print(f"Biggest gain: {max(changes):.1f} pp ({chart_data[0]['n']})")
    print(f"2024 max: {max(d['b'] for d in chart_data):.1f}%")
    return changes,


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — two time points across many entities
        - **Country selection**: Top 20 by 2024 share of territorial waters
        - **Story**: Kazakhstan jumped from 1% to 52.5%; several Latin American nations made big gains
        - **Color**: Large gains (>30pp) in orange-red, smaller gains cooler
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
