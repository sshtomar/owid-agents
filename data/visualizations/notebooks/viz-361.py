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
        # Energy Intensity of the Economy: 1990 vs 2022 — Methodology

        Documents how much energy economies use per unit of output, and how that changed.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-USE-COMM-GD-PP-KD.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    AGGREGATES = {'ZH','ZI','S3','B8','V2','Z4','4E','T4','Z7','7E','T7','EU','XD','XF','ZT','XI','XG','V3','ZJ','XJ','T2','XL','XO','XN','XQ','T3','XP','XU','OE','S4','V4','V1','S1','8S','T5','ZG','ZF','T6','XT','1W','XE','XM','ZQ','M2','M1','XY','EA'}

    countries = {}
    for r in data:
        if r['value'] is None: continue
        cc = r['country']
        if cc in AGGREGATES: continue
        if not cc.isalpha(): continue
        cn = r['countryName']
        if cc not in countries:
            countries[cc] = {'name': cn, 'pts': []}
        countries[cc]['pts'].append((r['year'], r['value']))

    results = []
    for cc, info in countries.items():
        pts = sorted(info['pts'], key=lambda x: x[0])
        yr1990 = next((v for y, v in pts if y == 1990), None)
        yr_recent = next((v for y, v in reversed(pts) if y >= 2020), None)
        if yr1990 is not None and yr_recent is not None:
            pct = (yr_recent - yr1990) / yr1990 * 100
            results.append({'n': info['name'], 'a': round(yr1990, 0), 'b': round(yr_recent, 0), 'pct': round(pct, 0)})

    results.sort(key=lambda x: x['a'], reverse=True)
    print(f"Countries with 1990 and recent data: {len(results)}")
    return (countries, results)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — extreme spread in 1990 values (Bosnia 653 vs Denmark 73) makes slope ideal for showing convergence
        - **Country selection**: Former Soviet/Eastern Bloc countries (started extremely high), major economies (Germany, Japan, France), and outlier Ireland
        - **Key insight**: Post-Soviet states had the most to gain — structural reforms eliminated wasteful Soviet-era industry; Ireland dropped 78% driven by services-led GDP growth (denominator effect)
        - **Color encoding**: Diverging green (biggest reducers) to red (increased)
        """
    )
    return


@app.cell
def _(json, results):
    KEEP = ['Bosnia and Herzegovina', 'China', 'Ethiopia', 'Belarus', 'Estonia', 'Armenia',
            'Kazakhstan', 'India', 'Germany', 'France', 'Japan', 'Ireland', 'Brazil', 'Denmark', 'Hong Kong SAR, China']

    chart_data = [r for r in results if any(k in r['n'] for k in KEEP)]
    for r in chart_data:
        r['n'] = (r['n']
            .replace('Bosnia and Herzegovina', 'Bosnia & Herz.')
            .replace('Hong Kong SAR, China', 'Hong Kong'))
    chart_data.sort(key=lambda x: x['a'], reverse=True)
    print(f"Final: {len(chart_data)} countries")
    print(json.dumps([{'n': r['n'], 'a': r['a'], 'b': r['b']} for r in chart_data], separators=(',', ':')))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
