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
        # Terrestrial Protected Areas — Methodology

        Slope chart comparing the share of total land under protection in 2013 vs 2024
        for the 20 countries with the highest 2024 protection levels.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--ER-LND-PTLD-ZS.json"
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
    print(f"Top 20 by 2024 value selected")
    return chart_data, slope, by_country, AGGREGATES


@app.cell
def _(chart_data):
    values_a = [d['a'] for d in chart_data]
    values_b = [d['b'] for d in chart_data]
    changes = [d['b'] - d['a'] for d in chart_data]
    print(f"2013 range: {min(values_a):.1f} – {max(values_a):.1f}%")
    print(f"2024 range: {min(values_b):.1f} – {max(values_b):.1f}%")
    print(f"Change range: {min(changes):.1f} – {max(changes):.1f} pp")
    return values_a, values_b, changes


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — comparing two time points across many entities
        - **Country selection**: Top 20 by 2024 protection share
        - **Color**: Change magnitude — large gains in orange/red, small changes in green/cool
        - **Highlights**: Bhutan doubled its coverage; Croatia, Cyprus, Armenia made large jumps
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
